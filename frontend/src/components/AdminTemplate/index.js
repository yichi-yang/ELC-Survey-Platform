import React, { useEffect, useState } from 'react';
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
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const pages = [];
const settings = ['Logout'];
const NAMES = ['Football','Basketball','Survey1','Survey2','Survey3'];

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

const AlertDialog =(props)=> {
  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div>
      <Button  variant="contained" size="small" style={{ background: '#990000'}} onClick={handleClickOpen}>
        {props.name}
      </Button>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          {"Warning..."}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            Do you want to {props.name} this Survey?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Decline</Button>
          <Button onClick={handleClose} autoFocus>
            Confirm
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

const AlertDialogRelease =(props)=> {
  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div>
      <Button  variant="contained" size="small" style={{ background: '#FFC72C'}} onClick={handleClickOpen}>
        {props.name}
      </Button>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          {"Warning..."}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            Do you want to {props.name} this Survey?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Decline</Button>
          <Button href={`released/${props.id}`} autoFocus>
            Confirm
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}


const SurveyBar = (props) => {
  const [open, setOpen] = React.useState(true);
    return (
      <Grid container columnSpacing={0.4}>
        <Grid item xs={4} style={{background:"C4C4C4",color:"black",textAlign:"center", fontSize: '1.5vw', fontWeight: "bold"}}>
          <Button variant="contained" disabled style={{color:'black', width:'25vw'}}>{props.name}</Button>
        </Grid>
        <Grid item xs={1.2}>
          <AlertDialog name="Update"/>
        </Grid>
        <Grid item xs={1.2}>
          <AlertDialog name="Delete"/>
        </Grid>
        <Grid item xs={1.2}>
          <AlertDialog name="Empty"/>
        </Grid>
        <Grid item xs={1.2}>
          <Button variant="contained" size="small" style={{ background: '#990000'}}>View</Button>
        </Grid>
        <Grid item xs={1.2}>
          <AlertDialogRelease name="Release" id={props.id}/>
        </Grid>
      </Grid>
    );
  }


export default function AdminTemplate(){
  const [surveyName, setsurveyName] = useState([]);
  const [surveyId, setSurveyId] = useState([]); 
  React.useEffect(() => {
  axios
   .get('/api/surveys/')
   .then((res) => {
    if (res.status === 200) {
      if(res.data.count>0){
        let nameList = [];
        let idList = [];
        res.data.results.forEach((q) => {
          if(!q.draft){
            nameList.push(q.title);
            idList.push(q.id);
          }
        });
        setsurveyName(nameList);
        setSurveyId(idList);
      }
    }
    }).catch((error) => { console.log(error) });
  }, []);
  console.log(surveyName)
  const navigate = useNavigate();
  return(
    <Grid container rowSpacing={2}>
      <Grid item xs={12}>
        <ResponsiveAppBar/>
      </Grid>
      <Grid item xs={9.5}>
        <strong style={{color:'black', fontSize: '1.5vw', marginLeft:'5vw'}}>Survey Template</strong>
      </Grid>
      
      <Grid item xs={2.5}>
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

      {surveyName.map((name,index) => (
        <Grid container style={{marginTop:'1.5vw'}}>
          <Grid item xs={1.5}></Grid>
          <Grid item xs={10.5}>
            <SurveyBar name={name} id={surveyId[index]}/>
          </Grid>
        </Grid>
      ))}
      
      
      <Grid item xs={10}></Grid>
      <Grid item xs={2}>

      <IconButton color="primary" aria-label="add to shopping cart" onClick={()=>{
        if(localStorage.getItem('surveyID')!==null){
          axios.delete(`/api/surveys/${localStorage.getItem('surveyID')}`).then(() => {
            localStorage.setItem('surveyID','null');
          });
        }
        navigate('/admin/create_survey');
      }}>

        <AddCircleOutlineIcon style={{color:'#FFC72C'}} sx={{ fontSize: 80 }}/>
      </IconButton>
      </Grid>
      
    </Grid>
  );
};

export {AdminTemplate, ResponsiveAppBar};
