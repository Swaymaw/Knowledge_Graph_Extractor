import React, {useState} from "react";
import Uploader from "./components/Uploader";
import Header from "./components/Header";
import TaskFiles from "./components/TaskFiles";
import Ribbon from "./components/Ribbon";
import Footer from "./components/Footer";

export default function App(){
  const [file, setFile] = useState(null);
  const [files_data, setData] = useState([])

  return (
    <div className="bg-dark">
      <Header/>
      <Uploader file={file} setFile={setFile} files_data={files_data} setData={setData}/>
      <Ribbon files_data={files_data} setData={setData}/>
      <TaskFiles file={file} setFile={setFile} files_data={files_data} setData={setData}/>
      <Footer/>
    </div>
  )
}
