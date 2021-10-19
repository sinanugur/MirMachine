
export class JobFetchError extends Error {
    constructor(message) {
        super(message)
        this.name = "JobFetchError"
    }
}

export class JobPostError extends Error {
    constructor(message) {
        super(message)
        this.name = "JobPostError"
    }
}

export class ResultFetchError extends Error {
    constructor(message) {
        super(message)
        this.name = "ResultFetchError"
    }
}