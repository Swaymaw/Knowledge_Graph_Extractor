import React from 'react'
import api from '../api'

export default function Uploader(props) {
    const {file, setFile, setData} = props

    const handleFileInputChange = (event) => {
        setFile(event.target.files[0])
    }

    const handleSubmit = async (event) => {
        event.preventDefault(); 

        const formData = new FormData(); 
        formData.append('file', file); 

        try {
            const response = await api.post("/uploadfile", formData)
            if (response) {
                console.log("File Uploaded Successfully")
            } else {
                console.log("Failed to Upload File")
            }
            api.get("/getall")
            .then( response => {
                setData(response.data.data.reverse()); 
            })
            .catch(error => {
                console.error(error)
            }); 
        } catch(error) {
            console.error(error)
        }
        setFile(null)
        event.target.reset()
    }
    
    return (
        <div>
            <h1 className='mt-5 text-center text-light'>Upload File</h1>
            <form onSubmit={handleSubmit}>
                <div style={{marginBottom: "20px"}}>
                    <input type="file" accept = "application/pdf" onChange={handleFileInputChange} className='form-control container'/>
                </div>
                <div className='text-center'>
                <button type="submit" className='btn btn-outline-primary float-center'>Upload</button>
                <p style={{display: 'inline-block'}} className='text-light mx-1'></p>
                </div>
            </form>
        </div>
    )
}
