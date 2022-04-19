import React, { useEffect, useState } from "react";
import { ResponsiveAppBar } from '../AdminTemplate';
import { useParams } from "react-router-dom";
import CircularProgress from '@mui/material/CircularProgress';
import axios from "axios";

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

const numberStyle = {
    fontSize: '2.5em'
}

function FormReleased() {
    const { surveyID } = useParams();
    const [code, setCode] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get(`/api/sessions/?survey=${surveyID}`)
            .then(response => {
                // remove any existing sessions
                if (response.data.results.length > 0) {
                    return axios.delete(`/api/sessions/${response.data.results[0].id}/`);
                } else {
                    return; // resolved promise
                }
            })
            .then(() => axios.post('/api/sessions/', { "survey": surveyID }))
            .then(response => {
                setCode(response.data.code);
            })
            .catch(error => {
                setError(String(error));
            });
    }, []);

    return (
        <div style={contentFormat}>
            <ResponsiveAppBar />
            <div style={titleFormat}><strong>Form Released</strong></div>
            <div style={background}>
                <div style={subtitle}>
                    <strong>
                        {error === null ? 'The Code for Form is' : error}
                    </strong>
                </div>
                <div style={numberStyle}>
                    {code !== null && <strong>{code}</strong>}
                    {(code ?? error) === null && <CircularProgress />}
                </div>
            </div>
        </div>
    )
}

export default FormReleased;