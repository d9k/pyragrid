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
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: article; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE article (
    id integer NOT NULL,
    name text,
    "systemName" text NOT NULL,
    path text,
    "activeRevisionId" integer,
    "isTemplate" boolean DEFAULT false NOT NULL,
    active boolean DEFAULT true NOT NULL
);


--
-- Name: article_revision; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE article_revision (
    id integer NOT NULL,
    "articleId" integer NOT NULL,
    "parentRevisionId" integer,
    code text NOT NULL,
    "dateTime" timestamp without time zone NOT NULL,
    "authorId" integer NOT NULL
);


--
-- Name: articles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE articles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: articles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE articles_id_seq OWNED BY article.id;


--
-- Name: articles_revisions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE articles_revisions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: articles_revisions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE articles_revisions_id_seq OWNED BY article_revision.id;


--
-- Name: good; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE good (
    id integer NOT NULL,
    name text NOT NULL,
    price numeric(12,2),
    "isEgood" boolean DEFAULT false NOT NULL,
    "filePath" text,
    active boolean DEFAULT false NOT NULL
);


--
-- Name: goods_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE goods_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: goods_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE goods_id_seq OWNED BY good.id;


--
-- Name: order; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE "order" (
    id integer NOT NULL,
    total real,
    paid_amount real,
    rejected_amount real,
    user_id integer
);


--
-- Name: order_good; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE order_good (
    id integer NOT NULL,
    order_id integer,
    status character varying(14),
    count real,
    total real,
    paid_amount real,
    refund_count real,
    refund_amount real,
    user_id integer,
    CONSTRAINT enum_order_status CHECK (((status)::text = ANY ((ARRAY['payment_failed'::character varying, 'excluded'::character varying, 'created'::character varying, 'refund_failed'::character varying, 'refund_began'::character varying, 'paid'::character varying, 'payment_began'::character varying, 'refunded'::character varying])::text[])))
);


--
-- Name: order_good_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE order_good_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: order_good_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE order_good_id_seq OWNED BY order_good.id;


--
-- Name: order_good_status; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE order_good_status (
    id integer NOT NULL,
    order_good_id integer,
    datetime timestamp without time zone NOT NULL,
    status character varying(14),
    paid real,
    rejected real,
    shop_money_delta real,
    user_id integer,
    CONSTRAINT enum_order_status CHECK (((status)::text = ANY ((ARRAY['payment_failed'::character varying, 'excluded'::character varying, 'created'::character varying, 'refund_failed'::character varying, 'refund_began'::character varying, 'paid'::character varying, 'payment_began'::character varying, 'refunded'::character varying])::text[])))
);


--
-- Name: order_good_status_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE order_good_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: order_good_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE order_good_status_id_seq OWNED BY order_good_status.id;


--
-- Name: order_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE order_id_seq OWNED BY "order".id;


--
-- Name: user_; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE user_ (
    id integer NOT NULL,
    vk_id bigint,
    login text,
    name text,
    email text,
    "group" text,
    email_check_code text,
    email_checked boolean DEFAULT false NOT NULL,
    active boolean DEFAULT false NOT NULL,
    password_hash text
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE users_id_seq OWNED BY user_.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY article ALTER COLUMN id SET DEFAULT nextval('articles_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY article_revision ALTER COLUMN id SET DEFAULT nextval('articles_revisions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY good ALTER COLUMN id SET DEFAULT nextval('goods_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "order" ALTER COLUMN id SET DEFAULT nextval('order_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY order_good ALTER COLUMN id SET DEFAULT nextval('order_good_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY order_good_status ALTER COLUMN id SET DEFAULT nextval('order_good_status_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY user_ ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY alembic_version (version_num) FROM stdin;
3ef35b74884
\.


--
-- Data for Name: article; Type: TABLE DATA; Schema: public; Owner: -
--

COPY article (id, name, "systemName", path, "activeRevisionId", "isTemplate", active) FROM stdin;
3	\N	index3	wut	4	f	f
1	\N	index	/tst/reroute	5	f	t
4	\N	index5	ttt	6	f	f
5	\N	i6	i6	7	f	f
6	\N	i7	/i7	8	f	f
7	\N	i8	\N	9	f	f
8	\N	i9	\N	10	f	f
9	\N	i10	\N	11	f	f
10	\N	i11	\N	12	f	f
11	\N	tst11	\N	13	f	f
\.


--
-- Data for Name: article_revision; Type: TABLE DATA; Schema: public; Owner: -
--

COPY article_revision (id, "articleId", "parentRevisionId", code, "dateTime", "authorId") FROM stdin;
2	1	\N	<div class="row"><div class="col-md-6 col-sm-6 col-xs-6 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>Lorem ipsum dolores</p></div></div><div class="col-md-6 col-sm-6 col-xs-6 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>azaza<br data-mce-bogus="1"></p></div></div></div>	2015-12-18 02:40:36.744713	5
3	1	2	<div class="row"><div class="col-md-6 col-sm-6 col-xs-6 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>Lorem ipsum dolores</p></div></div><div class="col-md-6 col-sm-6 col-xs-6 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>bangbang</p></div></div></div>	2015-12-21 01:04:31.237293	5
4	3	\N	<div class="row"><div class="col-md-6 col-sm-6 col-xs-6 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>Lorem ipsum dolores</p></div></div><div class="col-md-6 col-sm-6 col-xs-6 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>Lorem ipsum dolores</p></div></div></div>	2015-12-31 05:12:08.013058	5
5	1	3	<div class="row"><div class="col-md-6 col-sm-6 col-xs-6 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>Feuerwing<br data-mce-bogus="1"></p></div></div><div class="col-md-6 col-sm-6 col-xs-6 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>bangbang</p></div></div></div>	2015-12-31 05:17:13.71658	5
6	4	\N	<div class="row"><div class="col-md-12 col-sm-12 col-xs-12 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>Lorem ipsum dolores</p></div></div></div>	2015-12-31 05:40:19.06222	5
7	5	\N	<div class="row"><div class="col-md-12 col-sm-12 col-xs-12 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>Lorem ipsum dolores</p></div></div></div>	2015-12-31 05:41:39.329122	5
8	6	\N	<div class="row"><div class="col-md-12 col-sm-12 col-xs-12 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>Lorem ipsum dolores</p></div></div></div>	2015-12-31 05:50:19.540513	5
9	7	\N	<div class="row"><div class="col-md-12 col-sm-12 col-xs-12 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>Lorem ipsum dolores</p></div></div></div>	2015-12-31 06:07:54.370356	5
10	8	\N	<div class="row"><div class="col-md-12 col-sm-12 col-xs-12 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>Lorem ipsum dolores</p></div></div></div>	2015-12-31 06:08:09.148553	5
11	9	\N	<div class="row"><div class="col-md-12 col-sm-12 col-xs-12 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>Lorem ipsum dolores</p></div></div></div><div class="row"><div class="col-md-6 col-sm-6 col-xs-6 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>Lorem ipsum dolores</p></div></div><div class="col-md-6 col-sm-6 col-xs-6 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>Lorem ipsum dolores</p></div></div></div>	2015-12-31 06:09:40.081587	5
12	10	\N	<div class="row"><div class="col-md-12 col-sm-12 col-xs-12 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>Lorem ipsum dolores</p></div></div></div><div class="row"><div class="col-md-6 col-sm-6 col-xs-6 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>Lorem ipsum dolores</p></div></div><div class="col-md-6 col-sm-6 col-xs-6 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>Lorem ipsum dolores</p></div></div></div>	2015-12-31 06:10:29.509833	5
13	11	\N	<div class="row"><div class="col-md-12 col-sm-12 col-xs-12 column"><div data-ge-content-type="tinymce" class="ge-content ge-content-type-tinymce"><p>Lorem ipsum dolores</p></div></div></div>	2016-01-02 05:11:34.635537	5
\.


--
-- Name: articles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('articles_id_seq', 11, true);


--
-- Name: articles_revisions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('articles_revisions_id_seq', 13, true);


--
-- Data for Name: good; Type: TABLE DATA; Schema: public; Owner: -
--

COPY good (id, name, price, "isEgood", "filePath", active) FROM stdin;
1	Кирпич	10.00	f	\N	t
2	Тестовый файл	20.00	t	/texter.png	f
\.


--
-- Name: goods_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('goods_id_seq', 2, true);


--
-- Data for Name: order; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "order" (id, total, paid_amount, rejected_amount, user_id) FROM stdin;
\.


--
-- Data for Name: order_good; Type: TABLE DATA; Schema: public; Owner: -
--

COPY order_good (id, order_id, status, count, total, paid_amount, refund_count, refund_amount, user_id) FROM stdin;
\.


--
-- Name: order_good_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('order_good_id_seq', 1, false);


--
-- Data for Name: order_good_status; Type: TABLE DATA; Schema: public; Owner: -
--

COPY order_good_status (id, order_good_id, datetime, status, paid, rejected, shop_money_delta, user_id) FROM stdin;
\.


--
-- Name: order_good_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('order_good_status_id_seq', 1, false);


--
-- Name: order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('order_id_seq', 1, false);


--
-- Data for Name: user_; Type: TABLE DATA; Schema: public; Owner: -
--

COPY user_ (id, vk_id, login, name, email, "group", email_check_code, email_checked, active, password_hash) FROM stdin;
5	\N	admin	admin	noemail@changeme.org	admin	\N	t	t	622f887fddcbe559fa0675de486b3e39d33db28085526c8e38b9a32cf5598939:334a8639ab3b454e88e68af8853958de
1	\N	admin2	admin2	noemail@changeme.org	admin	\N	t	t	84f20f30a443e6d5c94c3ffe06ef8a4bc81c477938a76a88e7a18a3d2eb2b0ca:905f2d6994f2425fbc1490a5fbdb6e73
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('users_id_seq', 6, true);


--
-- Name: articles_path_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY article
    ADD CONSTRAINT articles_path_key UNIQUE (path);


--
-- Name: articles_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY article
    ADD CONSTRAINT articles_pkey PRIMARY KEY (id);


--
-- Name: articles_revisions_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY article_revision
    ADD CONSTRAINT articles_revisions_pkey PRIMARY KEY (id);


--
-- Name: articles_systemName_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY article
    ADD CONSTRAINT "articles_systemName_key" UNIQUE ("systemName");


--
-- Name: goods_name_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY good
    ADD CONSTRAINT goods_name_key UNIQUE (name);


--
-- Name: goods_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY good
    ADD CONSTRAINT goods_pkey PRIMARY KEY (id);


--
-- Name: order_good_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY order_good
    ADD CONSTRAINT order_good_pkey PRIMARY KEY (id);


--
-- Name: order_good_status_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY order_good_status
    ADD CONSTRAINT order_good_status_pkey PRIMARY KEY (id);


--
-- Name: order_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY "order"
    ADD CONSTRAINT order_pkey PRIMARY KEY (id);


--
-- Name: users_login_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY user_
    ADD CONSTRAINT users_login_key UNIQUE (login);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY user_
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_vk_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY user_
    ADD CONSTRAINT users_vk_id_key UNIQUE (vk_id);


--
-- Name: articles_revisions_articleId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY article_revision
    ADD CONSTRAINT "articles_revisions_articleId_fkey" FOREIGN KEY ("articleId") REFERENCES article(id);


--
-- Name: articles_revisions_authorId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY article_revision
    ADD CONSTRAINT "articles_revisions_authorId_fkey" FOREIGN KEY ("authorId") REFERENCES user_(id);


--
-- Name: order_good_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY order_good
    ADD CONSTRAINT order_good_order_id_fkey FOREIGN KEY (order_id) REFERENCES user_(id);


--
-- Name: order_good_status_order_good_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY order_good_status
    ADD CONSTRAINT order_good_status_order_good_id_fkey FOREIGN KEY (order_good_id) REFERENCES order_good(id);


--
-- Name: order_good_status_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY order_good_status
    ADD CONSTRAINT order_good_status_user_id_fkey FOREIGN KEY (user_id) REFERENCES user_(id);


--
-- Name: order_good_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY order_good
    ADD CONSTRAINT order_good_user_id_fkey FOREIGN KEY (user_id) REFERENCES user_(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: -
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

