import { Canvas } from 'reaflow'
import { useEffect, useState } from 'react'
import { fetchTree } from "../utils/Repository"

const Tree = (props) => {
    const [nodes, setNodes] = useState()
    const [edges, setEdges] = useState()

    useEffect(() => {
        const getNewickTree = async () => {
            let data = await fetchTree()
            console.log(data)
            setNodes(data.nodes)
            setEdges(data.edges)
        }
        getNewickTree()
    },[])
    return(
        <div>
            {nodes && edges &&
                <Canvas nodes={nodes} edges={edges}/>
            }
        </div>
    )
}

export default Tree
