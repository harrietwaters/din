import React from 'react';
import {
  Box,
  Button,
  ButtonGroup,
  FormControl,
  FormControlLabel,
  FormLabel,
  Grid,
  Paper,
  Radio,
  RadioGroup,
  withStyles,
  Typography
} from '@material-ui/core'

import IndeterminateCheckBoxIcon from '@material-ui/icons/IndeterminateCheckBox';
import AddBoxIcon from '@material-ui/icons/AddBox';

import axios from 'axios';
import { fontSize } from '@material-ui/system';

const styles = theme => ({
  root: {
    margin: '15%',
    height: '400px',
    width: '240px'
    // padding: theme.spacing(3, 2),
  },
  tempBox: {
    padding: theme.spacing(2),
    height: '60px',
    width: '130px'
  },
  info: {
    // borderStyle: 'solid',
    // borderColor: 'red',
    justify: 'left',
    textAlign: 'left',
    fontSize: 16,
  },
  currentTemp: {
    // borderStyle: 'solid',
    // borderColor: 'red',
    marginTop: '-20px',
    justify: 'right',
    textAlign: 'right',
    fontSize: 36,
  },
  targetTemp: {
    // borderStyle: 'solid',
    // borderColor: 'red',
    marginTop: '-8px',
    justify: 'right',
    textAlign: 'right',
    fontSize: 14,
  },
  buttonGroup: {
    margin: theme.spacing(1),
    display: 'block',
  }
});

axios.defaults.headers.post['Content-Type'] = 'application/json';

const HOST = 'http://192.168.1.254:5000/climate'

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentTemp: 0,
      targetTemp: 0,
      mode: 'cool',
      fanMode: 'auto'
    };

    this.incTemp = this.incTemp.bind(this);
    this.decTemp = this.decTemp.bind(this);
    this.setMode = this.setMode.bind(this);
    this.setFanMode = this.setFanMode.bind(this);
    this.update = this.update.bind(this);
  }

  timerId = 0

  componentDidMount() {
    const getClimate = () => {
      axios.get(HOST).then((resp) => {
        this.setState({
          currentTemp: parseInt(resp.data.current_temp),
          targetTemp: parseInt(resp.data.target_temp),
          mode: resp.data.thermostat_mode,
          fanMode: JSON.parse(resp.data.fan).fan_mode
        })
      });
    }
    getClimate();
    this.timerId = setInterval(getClimate, 30000);
  }

  componentWillUnmount() {
    clearInterval(this.timerId)
  }

  incTemp() {
    this.setState({ targetTemp: this.state.targetTemp + 1 })
    this.update({ target_temp: this.state.targetTemp + 1 })
  }


  decTemp() {
    this.setState({ targetTemp: this.state.targetTemp - 1 })
    this.update({ target_temp: this.state.targetTemp - 1 })
  }

  setMode(e) {
    e.persist();
    this.setState({ mode: e.target.value })
    this.update({ thermostat_mode: e.target.value })
  }

  setFanMode(e) {
    e.persist();
    this.setState({ fanMode: e.target.value })
    this.update({ fan_mode: e.target.value })
  }

  async update(updatedState) {
    const newState = Object.assign({
      target_temp: this.state.targetTemp,
      thermostat_mode: this.state.mode,
      fan_mode: this.state.fanMode
    },
      updatedState);

    console.dir(newState);

    const resp = await axios.post(HOST, newState, {
      headers: {
        'content-type': 'application/json'
      }
    });

    this.setState({
      currentTemp: parseInt(resp.data.current_temp),
      targetTemp: parseInt(resp.data.target_temp),
      mode: resp.data.thermostat_mode,
      fanMode: JSON.parse(resp.data.fan).fan_mode
    });
  }

  render() {
    const { classes } = this.props;
    return (
      <Grid container >


        <Paper className={classes.root}>
          <Grid container spacing={2}>
            <Grid item>
              <Box className={classes.tempBox}>
                <Typography className={classes.info}>Current: </Typography>
                <Typography className={classes.currentTemp} >{this.state.currentTemp}</Typography>
              </Box>
              <Typography className={classes.targetTemp}>Set to: {this.state.targetTemp}</Typography>
            </Grid>
            <Grid item>
              <ButtonGroup
                color='primary'
                variant='contained'
                size='large'
                align='center'
                className={classes.buttonGroup}>
                <Button onClick={this.incTemp}>
                  <AddBoxIcon></AddBoxIcon>
                </Button>
                <Button onClick={this.decTemp}>
                  <IndeterminateCheckBoxIcon></IndeterminateCheckBoxIcon>
                </Button>
              </ButtonGroup>
            </Grid>
          </Grid>
          <FormControl margin='normal'>
            <FormLabel>Mode</FormLabel>
            <RadioGroup row defaultValue={this.state.mode} name="thermostat_mode" value={this.state.mode} onChange={this.setMode}>
              <FormControlLabel value='cool' control={<Radio color='primary' />} label="Cool" />
              <FormControlLabel value='heat' control={<Radio color='primary' />} label="Heat" />
              <FormControlLabel value='off' control={<Radio color='primary' />} label="Off" />
            </RadioGroup>
          </FormControl>
          <FormControl>
            <FormLabel>Fan</FormLabel>
            <RadioGroup row defaultValue={this.state.fanMode} name="fan_mode" value={this.state.fanMode} onChange={this.setFanMode}>
              <FormControlLabel value='auto' control={<Radio color='primary' />} label="Auto" />
              <FormControlLabel value='on' control={<Radio color='primary' />} label="On" />
            </RadioGroup>
          </FormControl>
        </Paper>

        {/* <Grid item>
                <ButtonGroup color='primary'>
                  <Button variant='contained' onClick={this.incTemp}>
                    <AddBoxIcon></AddBoxIcon>
                  </Button>
                  <Button variant='contained' onClick={this.decTemp}>
                    <IndeterminateCheckBoxIcon></IndeterminateCheckBoxIcon>
                  </Button>
                </ButtonGroup>
              </Grid> */}

        {/* <FormControl>
              <FormLabel>Mode</FormLabel>
              <RadioGroup defaultValue={this.state.mode} name="thermostat_mode" value={this.state.mode} onChange={this.setMode}>
                <FormControlLabel value='cool' control={<Radio color='primary' />} label="Cool" />
                <FormControlLabel value='heat' control={<Radio color='primary' />} label="Heat" />
                <FormControlLabel value='off' control={<Radio color='primary' />} label="Off" />
              </RadioGroup>
            </FormControl>
            <FormControl>
              <FormLabel>Fan</FormLabel>
              <RadioGroup defaultValue={this.state.fanMode} name="fan_mode" value={this.state.fanMode} onChange={this.setFanMode}>
                <FormControlLabel value='auto' control={<Radio color='primary' />} label="Auto" />
                <FormControlLabel value='on' control={<Radio color='primary' />} label="On" />
              </RadioGroup>
            </FormControl> */}
      </Grid>
    );
  }
}

export default withStyles(styles)(App);
