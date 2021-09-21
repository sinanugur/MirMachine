import { Canvas, Node } from 'reaflow'

const Tree = (props) => {


    return(
        <div className={'modal'}>
            <div className={'canvas-container'}>
                <span className={'close'} onClick={() => {props.show(false)}}>&times;</span>
                <h3 className={'no-margins'}>Click on the node you wish to select</h3>
                {props.nodes && props.edges &&
                    <Canvas
                        nodes={props.nodes}
                        edges={props.edges}
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
