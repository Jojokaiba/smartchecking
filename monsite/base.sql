CREATE DATABASE admin;
\c admin;


CREATE TABLE mention (
    id_mention SERIAL PRIMARY KEY,
    nom_mention VARCHAR(100) NOT NULL
);


CREATE TABLE semestre (
    id_semestre SERIAL PRIMARY KEY,
    semestre VARCHAR(20),
    annee VARCHAR(20)
);


CREATE TABLE etudiant (
    id_etudiant SERIAL PRIMARY KEY,
    statut VARCHAR(50),
    matricule VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100),
    date_naissance DATE,
    genre VARCHAR(10),
    id_mention INT,
    id_semestre INT,

    CONSTRAINT fk_mention
        FOREIGN KEY (id_mention)
        REFERENCES mention(id_mention)
        ON DELETE SET NULL,

    CONSTRAINT fk_semestre
        FOREIGN KEY (id_semestre)
        REFERENCES semestre(id_semestre)
        ON DELETE SET NULL
);


CREATE TABLE matiere (
    id_matiere SERIAL PRIMARY KEY,
    nom_matiere VARCHAR(100) NOT NULL,
    id_semestre INT,
    id_mention INT,

    CONSTRAINT fk_matiere_semestre
        FOREIGN KEY (id_semestre)
        REFERENCES semestre(id_semestre)
        ON DELETE CASCADE,

    CONSTRAINT fk_matiere_mention
        FOREIGN KEY (id_mention)
        REFERENCES mention(id_mention)
        ON DELETE CASCADE
);




INSERT INTO mention (nom_mention)
VALUES 
('Informatique'),
('Gestion'),
('Droit'),
('Economie');


INSERT INTO semestre (semestre, annee)
VALUES
('S1', 'L1'),
('S2', 'L1'),
('S3', 'L2'),
('S4', 'L2'),
('S5', 'L3'),
('S6', 'L3');

INSERT INTO etudiant (statut,matricule, nom, prenom, date_naissance, genre, id_mention, id_semestre)
VALUES
('1','ETU001', 'Rakoto', 'Jean', '2002-05-12', 'M', 1, 1),
('1','ETU002', 'Rabe', 'Marie', '2003-01-20', 'F', 1, 1),
('2','ETU003', 'Randria', 'Paul', '2001-11-03', 'M', 2, 2),
('1','ETU004', 'Andriamanitra', 'Sofia', '2002-08-15', 'F', 3, 1);


INSERT INTO matiere (nom_matiere, id_semestre, id_mention)
VALUES
('Algorithmique', 1, 1),
('Programmation Java', 2, 1),
('Base de données', 1, 1),

('Comptabilité Générale', 1, 2),
('Management', 2, 2),

('Droit Civil', 1, 3),
('Microéconomie', 1, 4);



CREATE VIEW etudiant_all AS
SELECT
    e.id_etudiant,
    e.statut,
    e.matricule,
    e.nom,
    e.prenom,
    e.date_naissance,
    e.genre,
    m.nom_mention,
    s.semestre,
    s.annee

FROM etudiant e
LEFT JOIN mention m
    ON e.id_mention = m.id_mention
LEFT JOIN semestre s
    ON e.id_semestre = s.id_semestre;



CREATE VIEW matiere_all AS
SELECT
    ma.id_matiere,
    ma.nom_matiere as matiere,
    me.nom_mention as mention,
    se.semestre,
    se.annee

FROM matiere ma
LEFT JOIN mention me
    ON ma.id_mention = me.id_mention
LEFT JOIN semestre se
    ON ma.id_semestre = se.id_semestre;


SELECT *
FROM etudiant_all
WHERE
    (annee = 'L1' OR 'L1' IS NULL)
AND (nom_mention = 'Informatique' OR 'Informatique' IS NULL);
