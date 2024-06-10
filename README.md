# Knowledge Graph Builder 



#### KG Building Progress Steps after Document Upload
1) Text Extraction 
2) Text Cleanup 
3) Triplet Extraction using Stanford OpenIE

To view the knowledge graph the user clicks on the Graph button which appears when the status of triplet generation is completed and the knowledge graph is built on the go from the triplet after the button is pressed.


#### Steps to run the backend and frontend

```zsh
    docker run -dp 27017:27017 --name=<container-name> mongo:latest
    docker run -dp 6379:6379 --name=<container-name> -d redis:latest
    
    # or

    docker start e81d0233f061 602aecb8cc5d
    

    cd backend
    uvicorn main:app --reload
    celery -A task worker --loglevel=debug --concurrency=1 --pool=solo

    cd ..
    cd frontend 
    npm run dev

    # The Frontend Application Visible at - http://localhost:3000
```
