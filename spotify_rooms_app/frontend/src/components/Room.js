import React, { Component } from "react";
import { Grid, Button, Typography } from "@material-ui/core";
import { Link } from "react-router-dom";

export default class Room extends Component {
  constructor(props) {
    super(props);
    this.state = {
      votes_to_skip: 2,
      can_pause: false,
      is_host: false,
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

  render() {
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
        <Grid item xs={12}>
          <Button variant="contained" onClick={this.leaveBtnClicked}>
            Leave Room
          </Button>
        </Grid>
      </Grid>
    );
  }
}
