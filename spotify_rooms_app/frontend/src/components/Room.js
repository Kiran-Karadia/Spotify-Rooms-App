import React, { Component } from "react";
import { Grid, Button, Typography } from "@material-ui/core";
import { Link } from "react-router-dom";
import CreateRoomPage from "./CreateRoomPage";

export default class Room extends Component {
  constructor(props) {
    super(props);
    this.state = {
      votes_to_skip: 2,
      can_pause: false,
      is_host: false,
      show_settings: false,
    };
    this.room_code = this.props.match.params.room_code;
    this.getRoomDetails();
  }

  getRoomDetails() {
    fetch("/api/get-room" + "?room_code=" + this.room_code)
      .then((response) => {
        if (!response.ok) {
          this.props.leaveRoomCallback();
          this.props.history.push("/");
        }
        return response.json();
      })
      .then((data) => {
        this.setState({
          votes_to_skip: data.votes_to_skip,
          can_pause: data.can_pause,
          is_host: data.is_host,
        });
      });
  }

  leaveBtnClicked = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    };
    fetch("/api/leave-room", requestOptions).then((_response) => {
      this.props.leaveRoomCallback();
      this.props.history.push("/");
    });
  };

  showSettings = (value) => {
    this.setState({
      show_settings: value,
    });
  };

  renderSettings = () => {
    return (
      <Grid container spacing={1} align="center">
        <Grid item xs={12}>
          <CreateRoomPage
            update={true}
            votes_to_skip={this.state.votes_to_skip}
            can_pause={this.state.can_pause}
            room_code={this.room_code}
            updateCallback={null}
          />
        </Grid>
        <Grid item xs={12}>
          <Button variant="contained" onClick={() => this.showSettings(false)}>
            Return to room
          </Button>
        </Grid>
        <Grid item xs={12}></Grid>
        <Grid item xs={12}></Grid>
      </Grid>
    );
  };

  renderSettingsBtn() {
    return (
      <Grid item xs={12} align="center">
        <Button
          variant="contained"
          color="primary"
          onClick={() => this.showSettings(true)}
        >
          Settings
        </Button>
      </Grid>
    );
  }

  render() {
    if (this.state.show_settings) {
      return this.renderSettings();
    }
    return (
      <Grid container spacing={1} align="center">
        <Grid item xs={12}>
          <Typography variant="h4" component="h4">
            Code: {this.room_code}
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="h6" component="h6">
            Votes: {this.state.votes_to_skip}
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="h6" component="h6">
            Can Pause: {this.state.can_pause.toString()}
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="h6" component="h6">
            Host: {this.state.is_host.toString()}
          </Typography>
        </Grid>
        {this.state.is_host ? this.renderSettingsBtn() : null}
        <Grid item xs={12}>
          <Button variant="contained" onClick={this.leaveBtnClicked}>
            Leave Room
          </Button>
        </Grid>
      </Grid>
    );
  }
}
