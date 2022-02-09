import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import { styled, alpha } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import SearchIcon from '@mui/icons-material/Search';
import InputBase from '@mui/material/InputBase';
import Grid from '@mui/material/Grid';

const pages = [];
const settings = ['Logout'];
const NAMES = ['Football'];

const ResponsiveAppBar = () => {
  const [anchorElNav, setAnchorElNav] = React.useState(null);
  const [anchorElUser, setAnchorElUser] = React.useState(null);

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };
  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  return (
    <AppBar position="static" style={{ background: '#990000'}}>
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ mr: 1, display: { xs: 'none', md: 'flex' } }}
          >
            <strong style={{color:'#FFC72C', fontSize: '1.5vw'}}>Admin</strong>
          </Typography>

          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{
                display: { xs: 'block', md: 'none' },
              }}
            >
              {pages.map((page) => (
                <MenuItem key={page} onClick={handleCloseNavMenu}>
                  <Typography textAlign="center">{page}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}
          >
            <strong style={{color:'#FFC72C', fontSize: '2.5vw'}}>Admin</strong>
          </Typography>
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
            {pages.map((page) => (
              <Button
                key={page}
                onClick={handleCloseNavMenu}
                sx={{ my: 2, color: 'white', display: 'block' }}
              >
                {page}
              </Button>
            ))}
          </Box>

          <Box sx={{ flexGrow: 0 }}>
            <Tooltip title="Open settings">
              <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
              <Avatar sx={{ bgcolor: '#FFC72C' }}>A</Avatar>
              </IconButton>
            </Tooltip>
            <Menu
              sx={{ mt: '45px' }}
              id="menu-appbar"
              anchorEl={anchorElUser}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorElUser)}
              onClose={handleCloseUserMenu}
            >
              {settings.map((setting) => (
                <MenuItem key={setting} onClick={handleCloseUserMenu}>
                  <Typography textAlign="center">{setting}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
  },
  marginLeft: 0,
  width: '100%',
  [theme.breakpoints.up('sm')]: {
    marginLeft: theme.spacing(1),
    width: 'auto',
  },
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    // vertical padding + font size from searchIcon
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create('width'),
    width: '100%',
    [theme.breakpoints.up('sm')]: {
      width: '12ch',
      '&:focus': {
        width: '20ch',
      },
    },
  },
}));

const SurveyBar = (props) => {
  const [open, setOpen] = React.useState(true);
    return (
      <Grid container columnSpacing={0.4}>
        <Grid item xs={4} style={{background:"C4C4C4",color:"black",textAlign:"center", fontSize: '1.5vw', fontWeight: "bold"}}>
          <Button variant="contained" disabled style={{color:'black', width:'25vw'}}>{props.name}</Button>
        </Grid>
        <Grid item xs={1.2}>
          <Button variant="contained" size="small" onClick={() => { alert('Do you want to update Survey?');}} style={{ background: '#990000'}}>Update</Button>
        </Grid>
        <Grid item xs={1.2}>
          <Button variant="contained" size="small" onClick={() => { alert('Do you want to delete Surve?');}} style={{ background: '#990000'}}>Delete</Button>
        </Grid>
        <Grid item xs={1.2}>
          <Button variant="contained" size="small" onClick={() => { alert('Do you want to empty Surve?');}} style={{ background: '#990000'}}>Empty</Button>
        </Grid>
        <Grid item xs={1.2}>
          <Button variant="contained" size="small" style={{ background: '#990000'}}>View</Button>
        </Grid>
        <Grid item xs={1.2}>
          <Button variant="contained" size="small" onClick={() => { alert('Do you want to release Surve?');}} style={{ background: '#FFC72C'}}>Release</Button>
        </Grid>
      </Grid>
    );
  }


export default function AdminTemplate(){
  return(
    <Grid container rowSpacing={2}>
      <Grid item xs={12}>
        <ResponsiveAppBar/>
      </Grid>
      <Grid item xs={10}>
        <strong style={{color:'black', fontSize: '1.5vw', marginLeft:'5vw'}}>Survey Template</strong>
      </Grid>
      <Grid item xs={2}>
        <Search>
        <SearchIconWrapper>
        <SearchIcon />
        </SearchIconWrapper>
        <StyledInputBase
        placeholder="Search…"
        inputProps={{ 'aria-label': 'search' }}
        />
        </Search>
      </Grid>
      <Grid item xs={1}></Grid>
      <Grid item xs={11}>
        <SurveyBar name="Survey1"/>
      </Grid>
      <Grid item xs={1}></Grid>
      <Grid item xs={11}>
        <SurveyBar name="Survey2"/>
      </Grid>
      <Grid item xs={1}></Grid>
      <Grid item xs={11}>
        <SurveyBar name="Survey3"/>
      </Grid>
      <Grid item xs={1}></Grid>
      <Grid item xs={11}>
        <SurveyBar name="Survey4"/>
      </Grid>
      <Grid item xs={1}></Grid>
      <Grid item xs={11}>
        <SurveyBar name="Survey5"/>
      </Grid>
      <Grid item xs={1}></Grid>
      <Grid item xs={11}>
        <SurveyBar name="Survey6"/>
      </Grid>
      
    </Grid>
  );
};
