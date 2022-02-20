import axios from 'axios';
import jwt_decode from "jwt-decode";

const refreshWindow = 30; // try refresh the token 30s before it expires

let refreshRequest = Promise.resolve();

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

function getAccessToken() {
  // wait for previous refresh to finish
  return refreshRequest.then(() => {
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
          refreshRequest = axios.post('/api/auth/token/refresh/', {
            refresh: refreshToken
          }).then(res => {
            TokenStorage.setAccessToken(res.data.access);
            return res.data.access;
          });
          return refreshRequest;
        } else { // clear tokens if refresh token expired
          TokenStorage.clear()
        }
      }
    }
    return undefined;
  });
}

function registerTokenRefreshInterceptor() {
  axios.interceptors.request.use(config => {
    // skip all auth endpoints to avoid loops
    if (config.url.startsWith('/api/auth/')) {
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