--
-- PostgreSQL database dump
--

-- Dumped from database version 14.10 (Ubuntu 14.10-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.10 (Ubuntu 14.10-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: account; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account (
    account_id integer NOT NULL,
    username character varying,
    is_active boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.account OWNER TO postgres;

--
-- Name: account_account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.account_account_id_seq OWNER TO postgres;

--
-- Name: account_account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_account_id_seq OWNED BY public.account.account_id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: audiobook; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.audiobook (
    audiobook_id integer NOT NULL,
    category_id integer,
    title character varying(120) NOT NULL,
    author character varying(100) NOT NULL,
    description character varying(1000) NOT NULL,
    duration integer NOT NULL,
    cover_image character varying(2048) NOT NULL,
    listened_times integer,
    rating double precision,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.audiobook OWNER TO postgres;

--
-- Name: audiobook_audiobook_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.audiobook_audiobook_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.audiobook_audiobook_id_seq OWNER TO postgres;

--
-- Name: audiobook_audiobook_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.audiobook_audiobook_id_seq OWNED BY public.audiobook.audiobook_id;


--
-- Name: category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.category (
    category_id integer NOT NULL,
    name character varying NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.category OWNER TO postgres;

--
-- Name: category_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.category_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.category_category_id_seq OWNER TO postgres;

--
-- Name: category_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.category_category_id_seq OWNED BY public.category.category_id;


--
-- Name: user_settings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_settings (
    account_id integer NOT NULL,
    theme character varying(40),
    profile_picture character varying(2048),
    language character varying(40),
    wifi_only boolean,
    auto_play boolean,
    notifications_enabled boolean,
    adult_content_enabled boolean,
    explicit_phrases boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.user_settings OWNER TO postgres;

--
-- Name: account account_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account ALTER COLUMN account_id SET DEFAULT nextval('public.account_account_id_seq'::regclass);


--
-- Name: audiobook audiobook_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audiobook ALTER COLUMN audiobook_id SET DEFAULT nextval('public.audiobook_audiobook_id_seq'::regclass);


--
-- Name: category category_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category ALTER COLUMN category_id SET DEFAULT nextval('public.category_category_id_seq'::regclass);


--
-- Data for Name: account; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account (account_id, username, is_active, created_at, updated_at) FROM stdin;
1	dolphine	t	2024-01-07 18:01:41.501076	2024-01-07 18:01:41.501076
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
1347aa4629a1
\.


--
-- Data for Name: audiobook; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.audiobook (audiobook_id, category_id, title, author, description, duration, cover_image, listened_times, rating, created_at, updated_at) FROM stdin;
1	1	Sherlock Holmes	Doyle	What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.  Why do we use it? It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as th	300	https://marketplace.canva.com/EAFaQMYuZbo/1/0/1003w/canva-brown-rusty-mystery-novel-book-cover-hG1QhA7BiBU.jpg	0	0	2024-01-07 18:03:13.278335	2024-01-07 18:03:13.278335
2	2	Harry Potter	J.K. Rowling	What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.  Why do we use it? It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as th	320	https://bukovero.com/wp-content/uploads/2016/07/Harry_Potter_and_the_Cursed_Child_Special_Rehearsal_Edition_Book_Cover.jpg	0	0	2024-01-07 18:04:17.846022	2024-01-07 18:04:17.846022
3	3	Atomic Habits	Johan Koyle	What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.  Why do we use it? It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as th	350	https://d1csarkz8obe9u.cloudfront.net/posterpreviews/art-book-cover-design-template-34323b0f0734dccded21e0e3bebf004c_screen.jpg?ts=1637015198	0	0	2024-01-07 18:05:03.209817	2024-01-07 18:05:03.209817
\.


--
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.category (category_id, name, created_at, updated_at) FROM stdin;
1	Detective	2024-01-07 18:01:54.400868	2024-01-07 18:01:54.400868
2	Action	2024-01-07 18:02:04.440721	2024-01-07 18:02:04.440721
3	Horror	2024-01-07 18:02:27.385363	2024-01-07 18:02:27.385363
\.


--
-- Data for Name: user_settings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_settings (account_id, theme, profile_picture, language, wifi_only, auto_play, notifications_enabled, adult_content_enabled, explicit_phrases, created_at, updated_at) FROM stdin;
1	dark	https://yt3.googleusercontent.com/-CFTJHU7fEWb7BYEb6Jh9gm1EpetvVGQqtof0Rbh-VQRIznYYKJxCaqv_9HeBcmJmIsp2vOO9JU=s900-c-k-c0x00ffffff-no-rj	Uzbek	t	t	t	t	t	2024-01-07 18:06:33.324933	2024-01-07 18:06:33.324933
\.


--
-- Name: account_account_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_account_id_seq', 1, true);


--
-- Name: audiobook_audiobook_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.audiobook_audiobook_id_seq', 3, true);


--
-- Name: category_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.category_category_id_seq', 3, true);


--
-- Name: account account_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (account_id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: audiobook audiobook_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audiobook
    ADD CONSTRAINT audiobook_pkey PRIMARY KEY (audiobook_id);


--
-- Name: category category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (category_id);


--
-- Name: user_settings user_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_settings
    ADD CONSTRAINT user_settings_pkey PRIMARY KEY (account_id);


--
-- Name: ix_account_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_account_account_id ON public.account USING btree (account_id);


--
-- Name: ix_account_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_account_username ON public.account USING btree (username);


--
-- Name: ix_audiobook_audiobook_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_audiobook_audiobook_id ON public.audiobook USING btree (audiobook_id);


--
-- Name: ix_audiobook_author; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_audiobook_author ON public.audiobook USING btree (author);


--
-- Name: ix_audiobook_title; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_audiobook_title ON public.audiobook USING btree (title);


--
-- Name: ix_category_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_category_category_id ON public.category USING btree (category_id);


--
-- Name: ix_category_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_category_name ON public.category USING btree (name);


--
-- Name: audiobook audiobook_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audiobook
    ADD CONSTRAINT audiobook_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.category(category_id);


--
-- Name: user_settings user_settings_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_settings
    ADD CONSTRAINT user_settings_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(account_id);


--
-- PostgreSQL database dump complete
--

