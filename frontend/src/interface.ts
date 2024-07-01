export interface IRecord {
    id: number;
    name: string;
    revisions: number;
    created_at: Date;
    description: string;
}


export interface IForm {
    file: File,
    name: string;
    description: string;
    [key: string]: any
}