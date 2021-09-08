import { Canvas, Node } from 'reaflow'
import { useEffect, useState } from 'react'
import { fetchTree } from "../utils/Repository"

const Tree = (props) => {
    const [nodes, setNodes] = useState()
    const [edges, setEdges] = useState()
    useEffect(() => {
        const getNewickTree = async () => {
            let data = await fetchTree()
            setNodes(data.nodes)
            setEdges(data.edges)
        }
        getNewickTree()
    },[])
    return(
        <div className={'modal'}>
            <div className={'canvas-container'}>
                <span className={'close'} onClick={() => {props.show(false)}}>&times;</span>
                <h3 className={'no-margins'}>Click on the node you wish to select</h3>
                {nodes && edges &&
                    <Canvas
                        nodes={nodes}
                        edges={edges}
                        fit={true}
                        maxHeight={1800}
                        maxWidth={1600}
                        animated={false}
                        center={false}
                        node={
                            <Node onClick={(event,node) => {props.hook(node.id)}}/>
                        }
                    />
                }
            </div>
        </div>
    )
}

export default Tree
