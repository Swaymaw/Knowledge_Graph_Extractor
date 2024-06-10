import React, {useState} from 'react'
import api from '../api'

export default function Ribbon(props) {
    const {files_data, setData} = props

    const handleClear = async () => {
        if (confirm("This will delete all the information from the database. Are you sure you want to delete all the documents stored inside the database?")) {
                try {
                    const response = await api.delete("/reset_db")
                    if (response) {
                        console.log("DataBase Cleared")
                    } else {
                        console.log("DataBase Couldn't Be Cleared")
                    }
                } catch(error) {
                    console.error(error)
                }
        }
        handleRefresh()
    }
      
    const handleRefresh = () => {
            api.get("/getall")
            .then( response => {
                setData(response.data.data); 
            })
            .catch(error => {
                console.error(error)
            }); 
        }

    return (
        <div>
            <button className='btn btn-outline-primary float-end mx-3' onClick={() => handleClear()}>Clear</button>
            <button className='btn btn-outline-primary float-end mx-3' onClick={() => handleRefresh()}><i className='fa-solid fa-arrows-rotate'></i></button>
        </div>
    )
}
