import React from "react";
import { useState } from 'react';
import { ResponsiveAppBar } from '../AdminTemplate';

const contentFormat = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    flexDirection: 'column',
}

const titleFormat = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    margin: '5vw',
    fontSize: '1.6em',
}

const background = {
    display: 'flex',
    flexDirection: 'column',
    width: '60vw',
    height: '40vh',
    background: '#FFC72C',
    justifyContent: 'center',
    alignItems: 'center',
    color: 'white',
    fontSize: '2.4em',
}

const subtitle = {
    fontSize: '0.5em',
    color: 'black',
    padding: '1vw'
}

function FormReleased() {
    return(
        <div style={contentFormat}>
            <ResponsiveAppBar/>
            <div style={titleFormat}>Form Released</div>
            <div style={background}>
                <div style={subtitle}>The Code for Form is</div>
                <strong>
                    1234
                </strong>
            </div>
        </div>
    )
}

export default FormReleased;