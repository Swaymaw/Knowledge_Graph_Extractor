import React, {useState, useEffect} from 'react';
import { Modal, Button } from 'react-bootstrap';
import api from '../api';

function get_details(prog_string, file_status) {
    let msg = []

    if (file_status == "Uploaded") {
        for (let i = 0; i < prog_string.length; i++) {
            msg.push(<p style={{display: 'inline-block', color: 'gray'}}>Not Started</p>)
        }
    }

    if (file_status == "In Progress") {
        for (let i = 0; i < prog_string.length; i++) {
            if (prog_string[i] == 0) {
                msg.push(<p style={{display: 'inline-block', color: 'yellow'}}>In Progress</p>)

            } else {
                msg.push(<p style={{display: 'inline-block', color: 'green'}}>Completed</p>)
            }
        }
    }

    if (file_status == "Completed") {
        for (let i = 0; i < prog_string.length; i++) {
            msg.push(<p style={{display: 'inline-block', color: 'green'}}>Completed</p>)
        }
    }

    if (file_status == "Failed") {
        for (let i = 0; i < prog_string.length; i++) {
            if (prog_string[i] == 0) {
                msg.push(<p style={{display: 'inline-block', color: 'red'}}>Failed</p>)

            } else {
                msg.push(<p style={{display: 'inline-block', color: 'green'}}>Completed</p>)
            }
        }
    }

    return msg
}

export default function InfoModal({ show, handleClose, item }) {
    const [prog, setProg] = useState([0, 0, 0])
    const [file_status, setStatus] = useState(["Uploaded"])
    const handleRefresh = () => {
        api.get(`/getprogress?file_id=${item._id}`)
        .then( response => {
            setProg(response.data["File Content"])
            setStatus(response.data["File Status"])
        })
        .catch(error => {
            console.error(error)
        });
    }
    useEffect(() => {
        handleRefresh();
        // Set up the interval to fetch data every 10 seconds
        const intervalId = setInterval(handleRefresh, 1000);
        // Cleanup interval on component unmount
        return () => clearInterval(intervalId);
    }, []);

    const [val1, val2, val3] = get_details(prog, file_status)

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton className='custom-modal-close'>
                <Modal.Title className='text-light'>Item Information</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <p className='text-light'><strong>ID:</strong>{item._id}</p>
                <p className='text-light'><strong>Name:</strong>{item.name}</p>
                <p className='text-light mt-5'><strong>Text Extraction:</strong> {val1}</p>
                <p className='text-light'><strong>Text Cleanup:</strong> {val2}</p>
                <p className='text-light'><strong>Triplet Generation:</strong> {val3}</p>
            </Modal.Body>
            <Modal.Footer className='bg-dark'>
                <Button variant="outline-primary text-light" onClick={handleClose}>
                    Close
                </Button>
            </Modal.Footer>
        </Modal>
    );
}