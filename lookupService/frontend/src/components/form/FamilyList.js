import HelpText from './HelpText'

const FamilyList = (props) => {
    return(
        <div className={`optional-section optional-section__${props.showIncluded ? 'active' : 'passive'}`}>
                <span className={'default-margins pane-heading'}>
                    {props.node && 'Families that will be included in the search'}
                    {!props.node && 'Select a node and hit the refresh button'}
                    <HelpText text={'You can click on a family to view additional details in MirGeneDB'}/>
                </span>
            <span className={'button button--default'} onClick={async () => {
                props.handleIncludedFamilyFetching(true)
            }}>
                    Refresh
                </span>
            <div className={'scrolling-list-wrapped'}>
                {props.includedFamilies &&
                props.includedFamilies.families.map((it,i) => {
                    return <a key={i} href={`https://mirgenedb.org/browse/ALL?family=${it}`}
                              target={'_blank'}
                              className={'default-margins'}>{it}</a>
                })}
            </div>
        </div>
    )
}
export default FamilyList