import React from 'react';

import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import ToggleButton from 'react-bootstrap/ToggleButton';
import ToggleButtonGroup from 'react-bootstrap/ToggleButtonGroup';

import { Subject, of, interval } from 'rxjs';
import { map, merge, debounceTime } from 'rxjs/operators';

import axios from 'axios';
axios.defaults.headers.post['Content-Type'] = 'application/json';

const HOST = 'http://192.168.1.254/climate'

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentTemp: 0,
      targetTemp: 0,
      thermostatMode: 'cool',
      fanMode: 'auto'
    };

    this.changeState = new Subject();

    this.updateTimer = interval(30000);
  }

  timerId = 0;
  updateInProgress = false;
  updateResponses = [];

  componentDidMount() {
    this.changeState.pipe(
      map((value) => {
        this.setState(Object.assign(this.state, value));
        return value;
      }),
      debounceTime(300),
      map(() => {
        return axios.post(HOST, this.state);
      }),
      // Add in listeners for both our interval timer and a startup timer
      merge(
        this.updateTimer.pipe(
          merge(of('startup request')),
          map(() => {
            return axios.get(HOST);
          })
        )
      )
    ).subscribe(async (response) => {
      const { data: newState } = await response;
      this.setState({
        currentTemp: newState.currentTemp,
        targetTemp: newState.targetTemp,
        thermostatMode: newState.thermostatMode,
        fanMode: newState.fanMode
      });
    });
  }

  render() {
    return (
      <Container className='thermostat' style={{
        width: '30%',
        marginTop: '40%',
        padding: '40px',
        backgroundColor: 'lightGrey'
      }}>
        <Row xs={8}>
          <Col xs={7}
            style={{
              margin:'auto',
              marginLeft: '6%'
            }}>
            <Row
            style={{
              textAlign: 'right',
            }}>
              <h1>{this.state.currentTemp}</h1>
            </Row>
            <Row>
              Set to: {this.state.targetTemp}
            </Row>
          </Col>
          <Col xs={4}>
            <ButtonGroup vertical size='lg'>
              <Button onClick={() => this.changeState.next({ targetTemp: this.state.targetTemp + 1 })}>+</Button>
              <Button onClick={() => this.changeState.next({ targetTemp: this.state.targetTemp - 1 })}>-</Button>
            </ButtonGroup>
          </Col>
        </Row>
        <Row xs={6}>
          <ToggleButtonGroup
            type='radio'
            name='ThermostatMode'
            defaultValue={this.state.mode}
            value={this.state.mode}
            style={{
              width: '100rem'
            }}
            onChange={(e) => this.changeState.next({ thermostatMode: e })}>
            <ToggleButton value='cool'>Cool</ToggleButton>
            <ToggleButton value='heat'>Heat</ToggleButton>
            <ToggleButton value='off'>Off</ToggleButton>
          </ToggleButtonGroup>
        </Row>
        <Row xs={8}>
          <ToggleButtonGroup
            type='radio'
            name='FanMode'
            size='lg'
            defaultValue={this.state.fanMode}
            value={this.state.fanMode}
            style={{
              width: '100rem'
            }}
            onChange={(e) => this.changeState.next({ fanMode: e })}>
            <ToggleButton value='auto'>Auto</ToggleButton>
            <ToggleButton value='on'>On</ToggleButton>
          </ToggleButtonGroup>
        </Row>
      </Container>
    );
  }
}

export default App;
