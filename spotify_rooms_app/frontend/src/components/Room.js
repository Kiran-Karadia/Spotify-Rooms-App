import React, { Component } from "react";
import { Grid, Button, Typography } from "@material-ui/core";
import { Link } from "react-router-dom";
import CreateRoomPage from "./CreateRoomPage";
import MusicDisplay from "./MusicDisplay";

export default class Room extends Component {
  constructor(props) {
    super(props);
    this.state = {
      votes_to_skip: 2,
      can_pause: false,
      is_host: false,
      show_settings: false,
      spotify_auth: false,
      song: {}, // Store details about the song in the state, so that a new song will auto updat on the room page
    };
    this.room_code = this.props.match.params.room_code;
    this.getRoomDetails();
  }

  componentDidMount() {
    // When this component loads
    this.interval = setInterval(this.getCurrentSong, 1000); // Call this function every 1000ms (1 second)
  }

  componentWillUnmount() {
    // When the component is destroyed
    clearInterval(this.interval); // Clear interval
  }

  authenticateSpotify = () => {
    fetch("/spotify/is-authenticated")
      .then((response) => response.json())
      .then((data) => {
        this.setState({ spotify_auth: data.status });
        if (!data.status) {
          fetch("/spotify/get-auth-url")
            .then((response) => response.json())
            .then((data) => {
              window.location.replace(data.url);
            });
        }
      });
  };

  getCurrentSong = () => {
    fetch("/spotify/current-song")
      .then((response) => {
        if (!response.ok) {
          return {};
        } else {
          return response.json();
        }
      })
      .then((data) => {
        this.setState({ song: data });
        console.log(data);
      });
  };

  getRoomDetails = () => {
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
        if (this.state.is_host) {
          this.authenticateSpotify(); // Call this here becuase we need to wait for the room details, which tells us if the current user is a host
        }
      });
  };

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
            updateCallback={this.getRoomDetails}
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

  renderSettingsBtn = () => {
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
  };

  render = () => {
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
        <MusicDisplay {...this.state.song} />
        {this.state.is_host ? this.renderSettingsBtn() : null}
        <Grid item xs={12}>
          <Button variant="contained" onClick={this.leaveBtnClicked}>
            Leave Room
          </Button>
        </Grid>
      </Grid>
    );
  };
}
