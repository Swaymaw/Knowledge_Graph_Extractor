import React, {useEffect, useState} from 'react'
import api from '../api'
import InfoModal from './InfoModal';
import KnowledgeGraph from './KnowledgeGraph';

export default function TaskFiles(props) {
    const {files_data, setData} = props
    const [showModal, setShowModal] = useState(false);
    const [showGraph, setShowGraph] = useState(false);
    const [selectedItem, setSelectedItem] = useState(null);

    const handleRefresh = () => {
        api.get("/getall")
        .then( response => {
            setData(response.data.data.reverse()); 
        })
        .catch(error => {
            console.error(error)
        });
    }

    const handleStart = async (id) => {
        if (confirm(`This will start triplet generation for document ${id}. Are you sure you want to start the proccessing?`)) {
            try {
                const response = await api.put(`/fullpipeline?file_id=${id}`)
                if (response) {
                    console.log("Successfully started triplet generation")
                } else {
                    console.log("Couldn't Start Pipeline")
                }
            } catch(error) {
                console.error(error)
            }
        }
        handleRefresh()
    }

    useEffect(() => {
        handleRefresh();
        // Set up the interval to fetch data every 10 seconds
        const intervalId = setInterval(handleRefresh, 10000);
        // Cleanup interval on component unmount
        return () => clearInterval(intervalId);
    }, []);

    const handleDelete = async (id) => {
        if (confirm(`This will delete the all the data associated with document ${id}. Are you sure you want to delete this?`)) {
            try {
                response = await api.delete(`/delete_file?file_id=${id}`)
                if (response) {
                    console.log("Successfully deleted file")
                } else {
                    console.log("File Couldn't Be Deleted")
                }
            } catch(error) {
                console.error(error)
            }   
        }
        handleRefresh()
    }
    const handleShowModal = (item) => {
        setSelectedItem(item);
        setShowModal(true);
    };

    const handleCloseModal = () => {
        setShowModal(false);
        setSelectedItem(null);
    };

    const handleShowGraph = (item) => {
        setSelectedItem(item);
        setShowGraph(true);
    };

    const handleCloseGraph = () => {
        setShowGraph(false);
        setSelectedItem(null);
    };

    return (
        <div className="text-light">
            <table className="table table-dark my-5 table-container">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Created On</th>
                        <th>Job-ID</th>
                        <th>Progress</th>
                        <th>Status</th>
                        <th>Process</th>
                    </tr>
                </thead>
                <tbody>
                    {files_data.map((item, index) => (
                        <tr key={index}>
                            <td>{item._id} 
                                <button className='btn btn-dark' onClick={() => {handleDelete(item._id)}}>
                                    <i className='fa-solid fa-trash text-end'></i>
                                </button>
                            </td>
                            <td><p>{item.name}</p></td>
                            <td>{item.created_on.slice(0, 19)}</td>
                            <td>{item.job_id}</td>
                            <td className='text-center'>
                                <button className='btn btn-dark' onClick={() => handleShowModal(item)}>
                                    <i className='fa-solid fa-circle-info text-end'></i>
                                </button>
                            </td>
                            <td className='text-center'>
                                <p>{item.status}</p>
                                {item.status === 'Completed' && <button className='btn btn-outline-primary' onClick={() => handleShowGraph(item)}>GRAPH</button>}
                            </td>
                            <td className='text-center'>
                                {item.status == 'Completed' && <p className='mt-3'>Process Finished</p>}
                                {item.status != 'Completed' && <button className='btn btn-outline-primary' onClick={() => handleStart(item._id)}>START</button>}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            {selectedItem && <KnowledgeGraph show={showGraph} handleClose={handleCloseGraph} item={selectedItem} />}
            {selectedItem && <InfoModal show={showModal} handleClose={handleCloseModal} item={selectedItem} />}
            <br/>
        </div>
    )
}
