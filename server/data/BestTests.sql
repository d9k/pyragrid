--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: test_index_result; Type: TABLE; Schema: public; Owner: d9k; Tablespace: 
--

CREATE TABLE test_index_result (
    id integer NOT NULL,
    user_id integer,
    test_id integer,
    index_id integer
);


ALTER TABLE public.test_index_result OWNER TO d9k;

--
-- Name: test_index_result_id_seq; Type: SEQUENCE; Schema: public; Owner: d9k
--

CREATE SEQUENCE test_index_result_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.test_index_result_id_seq OWNER TO d9k;

--
-- Name: test_index_result_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: d9k
--

ALTER SEQUENCE test_index_result_id_seq OWNED BY test_index_result.id;


--
-- Name: tests; Type: TABLE; Schema: public; Owner: d9k; Tablespace: 
--

CREATE TABLE tests (
    id integer NOT NULL,
    name text,
    description text
);


ALTER TABLE public.tests OWNER TO d9k;

--
-- Name: tests_id_seq; Type: SEQUENCE; Schema: public; Owner: d9k
--

CREATE SEQUENCE tests_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tests_id_seq OWNER TO d9k;

--
-- Name: tests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: d9k
--

ALTER SEQUENCE tests_id_seq OWNED BY tests.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE users (
    id integer NOT NULL,
    vk_id bigint,
    name text
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: d9k
--

ALTER TABLE ONLY test_index_result ALTER COLUMN id SET DEFAULT nextval('test_index_result_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: d9k
--

ALTER TABLE ONLY tests ALTER COLUMN id SET DEFAULT nextval('tests_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Data for Name: test_index_result; Type: TABLE DATA; Schema: public; Owner: d9k
--

COPY test_index_result (id, user_id, test_id, index_id) FROM stdin;
\.


--
-- Name: test_index_result_id_seq; Type: SEQUENCE SET; Schema: public; Owner: d9k
--

SELECT pg_catalog.setval('test_index_result_id_seq', 1, false);


--
-- Data for Name: tests; Type: TABLE DATA; Schema: public; Owner: d9k
--

COPY tests (id, name, description) FROM stdin;
\.


--
-- Name: tests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: d9k
--

SELECT pg_catalog.setval('tests_id_seq', 1, false);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY users (id, vk_id, name) FROM stdin;
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('users_id_seq', 1, false);


--
-- Name: tests_pkey; Type: CONSTRAINT; Schema: public; Owner: d9k; Tablespace: 
--

ALTER TABLE ONLY tests
    ADD CONSTRAINT tests_pkey PRIMARY KEY (id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

