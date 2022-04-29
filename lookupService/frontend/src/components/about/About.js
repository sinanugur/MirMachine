

export const AboutPage = () => {
    return(
        <div className={'limit-width'}>
            <h2>About MirMachine</h2>
            <p>
                MirMachine is a phylogenetically informed microRNA annotation tool.<br/>
                It performs searches using covariance models based on the manually curated
                and evolutionarily informed microRNA database, <a href={'https://mirgenedb.org/'} target={'_blank'} className={'black-text'}>MirGeneDB</a>.<br/>
                The tool also calculates model-specific optimal score cut-off points to further increase accuracy. <br/>

                If you want to use the tool locally, download the <a href={'https://github.com/sinanugur/MirMachine'} target={'_blank'} className={'black-text'}>CLI tool </a>
                or our Docker image to run it on your local machine.<br/>
                This is especially useful if you possess a HPC unit. <br/><br/>

                If you encounter any bugs in the site, please submit an issue on the application's
                <a href={'https://github.com/selfjell/MirMachine'} target={'_blank'} className={'black-text'}> Github page</a>.
                <br/><br/>
                The MirMachine tool is created by Sinan Umu and Bastian Fromm.<br/>
                This application is created by Håvard Trondsen.
            </p>
            <h2>Using the tool</h2>
            <p>
                Although the application can handle larger queries, we specify that the human genome (~3.1GB) queried on ~250 families
                is a soft upper limit for what we can promise a reliable service for.<br/>
                If you have questions concerning individual input fields, you can click the question mark adjacent to the field.
                You do not have to provide a mail address.
                However, you must make sure to store the job ID safely so you are able to retrieve your job at a later stage.<br/>
                As our server has limited HPC slots, your job will be placed in a queue if the site experiences traffic.
                Your job will be initiated automatically once it reaches the front of the queue.<br/>
                You are also limited to one job submission at a time.
                Therefore, you must either cancel or wait for your ongoing to complete before submitting a new one.<br/>
                Remember to download your results once the job has been completed.
                As our server has limited storage space completed jobs will be deleted after four (4) days.
            </p>
        </div>
    )
}

