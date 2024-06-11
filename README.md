# Knowledge Graph Builder 



#### KG Building Progress Steps after Document Upload
1) Text Extraction 
2) Text Cleanup 
3) Triplet Extraction using Stanford OpenIE

To view the knowledge graph the user clicks on the Graph button which appears when the status of triplet generation is completed and the knowledge graph is built on the go from the triplet after the button is pressed.


#### Steps to run the backend and frontend
Run this from the root of the directory while making sure you don't have older images for mongo and redis.
This will run the application at http://localhost:3000

```zsh
    
    docker compose up 
```