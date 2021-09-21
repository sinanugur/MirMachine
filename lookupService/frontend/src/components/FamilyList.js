
const FamilyList = (props) => {
    return(
        <div className={`optional-section optional-section__${props.showIncluded ? 'active' : 'passive'}`}>
                <span className={'default-margins pane-heading'}>
                    {props.node && 'Families that will be included in the search'}
                    {!props.node && 'Select a node and hit the refresh button'}
                </span>
            <span className={'button button--default'} onClick={async () => {
                props.handleIncludedFamilyFetching(true)
            }}>
                    Refresh
                </span>
            <div className={'scrolling-list-wrapped'}>
                {props.includedFamilies &&
                props.includedFamilies.families.map((it,i) => {
                    return <span key={i} className={'default-margins'}>{it}</span>
                })}
            </div>
        </div>
    )
}
export default FamilyList