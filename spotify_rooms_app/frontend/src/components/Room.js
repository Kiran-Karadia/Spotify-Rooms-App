import React, { Component } from "react";

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
      .then((response) => response.json())
      .then((data) => {
        this.setState({
          votes_to_skip: data.votes_to_skip,
          can_pause: data.can_pause,
          is_host: data.is_host,
        });
      });
  }

  render() {
    return (
      <div>
        <h3>{this.room_code}</h3>
        <p>Votes: {this.state.votes_to_skip}</p>
        <p>Can Pause: {this.state.can_pause.toString()}</p>
        <p>Host: {this.state.is_host.toString()}</p>
      </div>
    );
  }
}
