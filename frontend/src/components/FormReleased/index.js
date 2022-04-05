import React, { useEffect, useState } from "react";
import { ResponsiveAppBar } from '../AdminTemplate';
import { useParams } from "react-router-dom";
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
    const {id} = useParams();
    const [code, setCode] = useState(undefined);

    useEffect(() => {

        axios.post('/api/sessions/',{"survey":id}).then(res=>{
            if(res.status===201){setCode(res.data.code)}})

    });

        
    return (
        <div style={contentFormat}>
            <ResponsiveAppBar />
            <div style={titleFormat}><strong>Form Released</strong></div>
            <div style={background}>
                <div style={subtitle}><strong>The Code for Form is</strong></div>
                <div style={numberStyle}>
                    <strong>
                        {code}
                    </strong>
                </div>
            </div>
        </div>
    )
}

export default FormReleased;