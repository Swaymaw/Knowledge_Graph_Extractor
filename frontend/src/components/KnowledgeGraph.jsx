import React, { useMemo } from 'react';
import { Modal, Button } from 'react-bootstrap';
import Graph from 'react-graph-vis';

export default function KnowledgeGraph({ show, handleClose, item }) {
    const getRandomColor = () =>  {
        var letters = '0123456789ABCDEF';
        var color = '#';
        for (var i = 0; i < 6; i++) {
          color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    const graphData = useMemo(() => {
        const nodes = {};
        const edges = [];

        // Convert graphData to nodes and edges
        item.triplets.forEach((data, index) => {
            if (!nodes[data.subject]) {
                nodes[data.subject] = { id: data.subject, label: data.subject, color: getRandomColor()};
            }
            if (!nodes[data.object]) {
                nodes[data.object] = { id: data.object, label: data.object };
            }
            edges.push({
                from: data.subject,
                to: data.object,
                label: data.relation
            });
        });

        return {
            nodes: Object.values(nodes),
            edges: edges
        };
    }, [item.triplets]);

    const options = useMemo(() => ({
        layout: {
            hierarchical: false
        },
        edges: {
            color: '#FFFFFF',
            arrows: {
                to: { enabled: true, scaleFactor: 1.2 }
            },
            smooth: {
                type: 'continuous',
                forceDirection: 'none',
                roundness: 0.5
            }
        },
        physics: {
            enabled: true,
            solver: 'forceAtlas2Based',
            forceAtlas2Based: {
                gravitationalConstant: -100,
                centralGravity: 0.01,
                springLength: 200,
                springConstant: 0.08,
                damping: 0.4,
                avoidOverlap: 1
            },
            maxVelocity: 50,
            minVelocity: 0.1,
            stabilization: {
                enabled: true,
                iterations: 200,
                updateInterval: 25
            },
            timestep: 0.5,
            adaptiveTimestep: true
        },
        interaction: {
            dragNodes: true,
            hideEdgesOnDrag: true,
            hideNodesOnDrag: false
        }
    }), []);


    return (
        <Modal show={show} onHide={handleClose} size="xl">
            <Modal.Header closeButton className='custom-modal-close'>
                <Modal.Title className='text-light'>Knowledge Graph</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <p className='text-light'><strong>ID:</strong> {item._id}</p>
                <p className='text-light'><strong>Name:</strong> {item.name}</p>
                <div style={{ height: '400px' }}>
                    <Graph 
                        graph={graphData}
                        options={options}
                        style={{ height: "100%" }}
                    />
                </div>
            </Modal.Body>
            <Modal.Footer className='bg-dark'>
                <Button variant="outline-primary text-light" onClick={handleClose}>
                    Close
                </Button>
            </Modal.Footer>
        </Modal>
    );
}
