import axios from 'axios';
import jwt_decode from "jwt-decode";

const refreshWindow = 30; // try refresh the token 30s before it expires

function secondsBeforeExpire(jwt) {
  return jwt_decode(jwt).exp - Date.now() / 1000;
}

const TokenStorage = {

  getRefreshToken() {
    return localStorage.getItem('refresh_token');
  },

  getAccessToken() {
    return localStorage.getItem('access_token');
  },

  setRefreshToken(token) {
    localStorage.setItem('refresh_token', token);
  },

  setAccessToken(token) {
    localStorage.setItem('access_token', token);
  },

  clear() {
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('access_token');
  },

  isLoggedIn() {
    const refreshToken = this.getRefreshToken();
    if (refreshToken) {
      if (secondsBeforeExpire(refreshToken) < 0) {
        return true;
      } else {
        this.clear();
      }
    }
    return false;
  }
}

let prevGetTokenPromise = Promise.resolve();

function getAccessToken() {
  // wait for previous refresh to finish
  const getTokenPromise = prevGetTokenPromise.then(() => {
    const accessToken = TokenStorage.getAccessToken();
    if (accessToken) {
      // check if the access token is about to expire
      if (secondsBeforeExpire(accessToken) >= refreshWindow) {
        // if accessToken will stay valid for at least refreshWindow seconds
        return accessToken;
      } else {
        // we better refresh the token now
        const refreshToken = TokenStorage.getRefreshToken();
        // check if the refresh token is valid
        if (refreshToken && secondsBeforeExpire(refreshToken) > 0) {
          // refresh the access token
          return axios.post(
            '/api/auth/token/refresh/',
            { refresh: refreshToken },
            { useJWT: false }
          ).then(res => {
            TokenStorage.setAccessToken(res.data.access);
            return res.data.access;
          });
        } else { // clear tokens if refresh token expired
          TokenStorage.clear()
        }
      }
    }
    return undefined;
  }).catch(e => {
    // handle error to not stall the chain
    console.log('Refresh access token failed with error:', e);
  });
  prevGetTokenPromise = getTokenPromise;
  return getTokenPromise;
}

function registerTokenRefreshInterceptor() {
  axios.interceptors.request.use(config => {
    // skip requests with useJWT set to false
    if (config.useJWT === false) {
      return config;
    }
    return getAccessToken().then(accessToken => {
      if (accessToken) {
        config.headers['Authorization'] = 'Bearer ' + accessToken;
      }
      return config;
    })
  });
}

export { registerTokenRefreshInterceptor, TokenStorage };