import React from "react";

export default function ConfirmationPage(props) {
    const bodyStyle = {
        display: 'flex',
        backgroundColor: '#D1D1D1',
        alighItems: 'center',
        justifyContent: 'center',
        flexWrap: 'wrap',
    }

    const headingStyle = {
        height: '15vh',
        width: '100vw',
        color: 'white',
        backgroundColor: '#990000',
        margin: '0',
        padding: '0',
        fontSize: '1.6em',
        textAlign: 'center',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        top: '0',
    };

    /* Adjust for iPhone minWidth 360 */
    const content = {
        display: 'flex',
        backgroundColor: 'white',
        minHeight: '100vh',
        justifyContent: 'center',
        textAlign: 'center',
        width: '60%',
        minWidth: 360,
        flexDirection: 'column'
    }

    const successStyle = {
        flexDirection: 'column',
        margin: '3vw',
        color: 'green'
    }

    const submitButton = {
        backgroundColor: '#FFC72C',
        textAlign: 'center',
        color: 'white',
        marginTop: '5vh',
        border: 0,
        height: 40,
        fontSize: '1em',
        width: '100%',
        cursor: 'pointer'
    };


    return (
        <div style={bodyStyle}>
            <div style={headingStyle}>
                <strong>Confirmation Page</strong>
            </div>
            <div style={content}>
                <div style={successStyle}>You have successfully submitted the form!</div>

                <a href="student"> 
                    <button id="back" style={submitButton}>
                        <strong>Back to Log in Page</strong>
                    </button>
                </a>
                
            </div>
        </div>
    );
};