export interface Client {
  dni: string;
  name: string;
  surname: string;
  address: string;
  birthDate: string;
}

export interface User {
  id: number;
  username: string;
}

export interface Project {
  title: string;
  description: string;
  level: number;
  initDate: string;
  finDate: string;
  report?: string;
  is_finalized: boolean;
  idCategory: number;
}

export interface Projects{
    projects: Project[];
}