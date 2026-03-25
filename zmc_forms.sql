--
-- PostgreSQL database dump
--

\restrict zzMfIBFygmiwZZuCapfa4kTKFYhSEQiSggYYfBzJ3OfHdlihmq23UOpDgoHzja5

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: extracted_records; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.extracted_records (
    id integer NOT NULL,
    submission_id integer NOT NULL,
    form_type_id integer,
    filename character varying(300),
    image_path character varying(500),
    raw_extraction text,
    verified_data text,
    status character varying(50),
    error_message text,
    confidence double precision,
    created_at timestamp without time zone,
    saved_at timestamp without time zone
);


ALTER TABLE public.extracted_records OWNER TO postgres;

--
-- Name: extracted_records_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.extracted_records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.extracted_records_id_seq OWNER TO postgres;

--
-- Name: extracted_records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.extracted_records_id_seq OWNED BY public.extracted_records.id;


--
-- Name: field_configs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.field_configs (
    id integer NOT NULL,
    form_type_id integer NOT NULL,
    key character varying(100) NOT NULL,
    label character varying(200) NOT NULL,
    field_type character varying(50),
    enabled boolean,
    "order" integer
);


ALTER TABLE public.field_configs OWNER TO postgres;

--
-- Name: field_configs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.field_configs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.field_configs_id_seq OWNER TO postgres;

--
-- Name: field_configs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.field_configs_id_seq OWNED BY public.field_configs.id;


--
-- Name: flexo_printing_records; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.flexo_printing_records (
    id integer NOT NULL,
    extracted_record_id integer,
    saved_at timestamp without time zone,
    date character varying(50),
    job_name character varying(200),
    job_code character varying(100),
    party_name character varying(200),
    operator character varying(200),
    material character varying(200),
    supplier character varying(200),
    rm_number character varying(100),
    order_qty double precision,
    web_size character varying(100),
    mic character varying(100),
    cylinder_size character varying(100),
    no_of_colors double precision,
    ink_gsm double precision,
    speed double precision,
    block_number character varying(100),
    tube_sheet character varying(100),
    bag_size character varying(100),
    setting_time character varying(100),
    start_time character varying(100),
    end_time character varying(100),
    plain_roll_wt double precision,
    plain_bal double precision,
    printed_roll_number character varying(200),
    printed_reel_wt double precision,
    core_wt double precision,
    counter_meter character varying(200),
    balance_rejected character varying(200),
    gross_wt double precision,
    net_wt double precision,
    total_counter double precision,
    total_meter double precision,
    setting_waste double precision,
    roll_waste double precision,
    printed_waste double precision,
    plain_waste double precision,
    total_waste double precision,
    rejected_core_wt double precision,
    prepared_by character varying(200),
    supervisor character varying(200),
    remarks text
);


ALTER TABLE public.flexo_printing_records OWNER TO postgres;

--
-- Name: flexo_printing_records_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.flexo_printing_records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.flexo_printing_records_id_seq OWNER TO postgres;

--
-- Name: flexo_printing_records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.flexo_printing_records_id_seq OWNED BY public.flexo_printing_records.id;


--
-- Name: form_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.form_types (
    id integer NOT NULL,
    code character varying(50) NOT NULL,
    name character varying(200) NOT NULL,
    keywords text,
    created_at timestamp without time zone
);


ALTER TABLE public.form_types OWNER TO postgres;

--
-- Name: form_types_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.form_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.form_types_id_seq OWNER TO postgres;

--
-- Name: form_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.form_types_id_seq OWNED BY public.form_types.id;


--
-- Name: gravure_printing_records; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gravure_printing_records (
    id integer NOT NULL,
    extracted_record_id integer,
    saved_at timestamp without time zone,
    print_date character varying(50),
    job_name character varying(200),
    job_code character varying(100),
    material character varying(200),
    supplier character varying(200),
    rm_number character varying(100),
    plain_order_qty double precision,
    web_size_mic character varying(200),
    cylinder_qty_number character varying(200),
    cylinder_length_cir character varying(200),
    operator character varying(200),
    color_man_ink_gsm character varying(200),
    speed double precision,
    setting_time character varying(100),
    start_time character varying(100),
    end_time character varying(100),
    plain_roll_wt double precision,
    plain_balance double precision,
    plain_core_wt double precision,
    printed_roll_number character varying(200),
    printed_roll_wt double precision,
    printed_core_wt double precision,
    meter double precision,
    balance double precision,
    rejected double precision,
    gross_wt double precision,
    net_wt double precision,
    total_mtr double precision,
    plain_waste double precision,
    roll_waste double precision,
    printed_waste double precision,
    setting_waste double precision,
    total_waste_core_wt double precision,
    total_waste_net_wt double precision,
    prepared_by character varying(200),
    supervisor character varying(200),
    remarks text
);


ALTER TABLE public.gravure_printing_records OWNER TO postgres;

--
-- Name: gravure_printing_records_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.gravure_printing_records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gravure_printing_records_id_seq OWNER TO postgres;

--
-- Name: gravure_printing_records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.gravure_printing_records_id_seq OWNED BY public.gravure_printing_records.id;


--
-- Name: submissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.submissions (
    id integer NOT NULL,
    batch_id character varying(100) NOT NULL,
    uploaded_at timestamp without time zone,
    status character varying(50)
);


ALTER TABLE public.submissions OWNER TO postgres;

--
-- Name: submissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.submissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.submissions_id_seq OWNER TO postgres;

--
-- Name: submissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.submissions_id_seq OWNED BY public.submissions.id;


--
-- Name: extracted_records id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracted_records ALTER COLUMN id SET DEFAULT nextval('public.extracted_records_id_seq'::regclass);


--
-- Name: field_configs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field_configs ALTER COLUMN id SET DEFAULT nextval('public.field_configs_id_seq'::regclass);


--
-- Name: flexo_printing_records id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.flexo_printing_records ALTER COLUMN id SET DEFAULT nextval('public.flexo_printing_records_id_seq'::regclass);


--
-- Name: form_types id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_types ALTER COLUMN id SET DEFAULT nextval('public.form_types_id_seq'::regclass);


--
-- Name: gravure_printing_records id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gravure_printing_records ALTER COLUMN id SET DEFAULT nextval('public.gravure_printing_records_id_seq'::regclass);


--
-- Name: submissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submissions ALTER COLUMN id SET DEFAULT nextval('public.submissions_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: extracted_records; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.extracted_records (id, submission_id, form_type_id, filename, image_path, raw_extraction, verified_data, status, error_message, confidence, created_at, saved_at) FROM stdin;
\.


--
-- Data for Name: field_configs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.field_configs (id, form_type_id, key, label, field_type, enabled, "order") FROM stdin;
1	1	date	Date	date	t	1
2	1	job_name	Job Name	text	t	2
3	1	job_code	Job Code	text	t	3
4	1	party_name	Party Name	text	t	4
5	1	operator	Operator	text	t	5
6	1	material	Material	text	t	6
7	1	supplier	Supplier	text	t	7
8	1	rm_number	R.M #	text	t	8
9	1	order_qty	Order Qty	number	t	9
10	1	web_size	Web Size	text	t	10
11	1	mic	Mic	text	t	11
12	1	cylinder_size	Cylinder Size	text	t	12
13	1	no_of_colors	No. of Colors	number	t	13
14	1	ink_gsm	Ink GSM	number	t	14
15	1	speed	Speed	number	t	15
16	1	block_number	Block #	text	t	16
17	1	tube_sheet	Tube/Sheet	text	t	17
18	1	bag_size	Bag Size	text	t	18
19	1	setting_time	Setting Time	text	t	19
20	1	start_time	Start Time	text	t	20
21	1	end_time	End Time	text	t	21
22	1	plain_roll_wt	Plain Roll Wt.	number	t	22
23	1	plain_bal	Plain Balance	number	t	23
24	1	printed_roll_number	Printed Roll #	text	t	24
25	1	printed_reel_wt	Printed Reel Wt.	number	t	25
26	1	core_wt	Core Wt.	number	t	26
27	1	counter_meter	Counter / Meter	text	t	27
28	1	balance_rejected	Balance / Rejected	text	t	28
29	1	gross_wt	Gross Wt.	number	t	29
30	1	net_wt	Net Wt.	number	t	30
31	1	total_counter	Total Counter	number	t	31
32	1	total_meter	Total Meter	number	t	32
33	1	setting_waste	Setting Waste	number	t	33
34	1	roll_waste	Roll Waste	number	t	34
35	1	printed_waste	Printed Waste	number	t	35
36	1	plain_waste	Plain Waste	number	t	36
37	1	total_waste	Total Waste	number	t	37
38	1	rejected_core_wt	Rejected Core Wt.	number	t	38
39	1	prepared_by	Prepared By	text	t	39
40	1	supervisor	Supervisor	text	t	40
41	1	remarks	Remarks	text	t	41
42	2	print_date	Print Date	date	t	1
43	2	job_name	Job Name	text	t	2
44	2	job_code	Job Code	text	t	3
45	2	material	Material	text	t	4
46	2	supplier	Supplier	text	t	5
47	2	rm_number	R.M #	text	t	6
48	2	plain_order_qty	Plain Order Qty	number	t	7
49	2	web_size_mic	Web Size & Mic	text	t	8
50	2	cylinder_qty_number	Cylinder Qty & #	text	t	9
51	2	cylinder_length_cir	Cylinder Length x Cir	text	t	10
52	2	operator	Operator	text	t	11
53	2	color_man_ink_gsm	Color Man Ink GSM	text	t	12
54	2	speed	Speed	number	t	13
55	2	setting_time	Setting Time	text	t	14
56	2	start_time	Start Time	text	t	15
57	2	end_time	End Time	text	t	16
58	2	plain_roll_wt	Plain Roll Wt.	number	t	17
59	2	plain_balance	Plain Balance	number	t	18
60	2	plain_core_wt	Plain Core Wt.	number	t	19
61	2	printed_roll_number	Printed Roll #	text	t	20
62	2	printed_roll_wt	Printed Roll Wt.	number	t	21
63	2	printed_core_wt	Printed Core Wt.	number	t	22
64	2	meter	Meter	number	t	23
65	2	balance	Balance	number	t	24
66	2	rejected	Rejected	number	t	25
67	2	gross_wt	Gross Wt.	number	t	26
68	2	net_wt	Net Wt.	number	t	27
69	2	total_mtr	Total Mtr.	number	t	28
70	2	plain_waste	Plain Waste	number	t	29
71	2	roll_waste	Roll Waste	number	t	30
72	2	printed_waste	Printed Waste	number	t	31
73	2	setting_waste	Setting Waste	number	t	32
74	2	total_waste_core_wt	Total Waste Core Wt.	number	t	33
75	2	total_waste_net_wt	Total Waste Net Wt.	number	t	34
76	2	prepared_by	Prepared By	text	t	35
77	2	supervisor	Supervisor	text	t	36
78	2	remarks	Remarks	text	t	37
\.


--
-- Data for Name: flexo_printing_records; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.flexo_printing_records (id, extracted_record_id, saved_at, date, job_name, job_code, party_name, operator, material, supplier, rm_number, order_qty, web_size, mic, cylinder_size, no_of_colors, ink_gsm, speed, block_number, tube_sheet, bag_size, setting_time, start_time, end_time, plain_roll_wt, plain_bal, printed_roll_number, printed_reel_wt, core_wt, counter_meter, balance_rejected, gross_wt, net_wt, total_counter, total_meter, setting_waste, roll_waste, printed_waste, plain_waste, total_waste, rejected_core_wt, prepared_by, supervisor, remarks) FROM stdin;
\.


--
-- Data for Name: form_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.form_types (id, code, name, keywords, created_at) FROM stdin;
1	F-PRD/01.2	Flexo Printing Production Report	flexo,F-PRD/01.2,flexo printing	2026-03-01 14:33:22.797001
2	F-PRD/01.1	Gravure Printing Production Report	gravure,F-PRD/01.1,gravure printing	2026-03-01 14:33:22.815227
\.


--
-- Data for Name: gravure_printing_records; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gravure_printing_records (id, extracted_record_id, saved_at, print_date, job_name, job_code, material, supplier, rm_number, plain_order_qty, web_size_mic, cylinder_qty_number, cylinder_length_cir, operator, color_man_ink_gsm, speed, setting_time, start_time, end_time, plain_roll_wt, plain_balance, plain_core_wt, printed_roll_number, printed_roll_wt, printed_core_wt, meter, balance, rejected, gross_wt, net_wt, total_mtr, plain_waste, roll_waste, printed_waste, setting_waste, total_waste_core_wt, total_waste_net_wt, prepared_by, supervisor, remarks) FROM stdin;
\.


--
-- Data for Name: submissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.submissions (id, batch_id, uploaded_at, status) FROM stdin;
\.


--
-- Name: extracted_records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.extracted_records_id_seq', 23, true);


--
-- Name: field_configs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.field_configs_id_seq', 78, true);


--
-- Name: flexo_printing_records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.flexo_printing_records_id_seq', 4, true);


--
-- Name: form_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.form_types_id_seq', 2, true);


--
-- Name: gravure_printing_records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.gravure_printing_records_id_seq', 2, true);


--
-- Name: submissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.submissions_id_seq', 9, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: extracted_records extracted_records_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracted_records
    ADD CONSTRAINT extracted_records_pkey PRIMARY KEY (id);


--
-- Name: field_configs field_configs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field_configs
    ADD CONSTRAINT field_configs_pkey PRIMARY KEY (id);


--
-- Name: flexo_printing_records flexo_printing_records_extracted_record_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.flexo_printing_records
    ADD CONSTRAINT flexo_printing_records_extracted_record_id_key UNIQUE (extracted_record_id);


--
-- Name: flexo_printing_records flexo_printing_records_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.flexo_printing_records
    ADD CONSTRAINT flexo_printing_records_pkey PRIMARY KEY (id);


--
-- Name: form_types form_types_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_types
    ADD CONSTRAINT form_types_code_key UNIQUE (code);


--
-- Name: form_types form_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_types
    ADD CONSTRAINT form_types_pkey PRIMARY KEY (id);


--
-- Name: gravure_printing_records gravure_printing_records_extracted_record_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gravure_printing_records
    ADD CONSTRAINT gravure_printing_records_extracted_record_id_key UNIQUE (extracted_record_id);


--
-- Name: gravure_printing_records gravure_printing_records_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gravure_printing_records
    ADD CONSTRAINT gravure_printing_records_pkey PRIMARY KEY (id);


--
-- Name: submissions submissions_batch_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submissions
    ADD CONSTRAINT submissions_batch_id_key UNIQUE (batch_id);


--
-- Name: submissions submissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submissions
    ADD CONSTRAINT submissions_pkey PRIMARY KEY (id);


--
-- Name: extracted_records extracted_records_form_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracted_records
    ADD CONSTRAINT extracted_records_form_type_id_fkey FOREIGN KEY (form_type_id) REFERENCES public.form_types(id);


--
-- Name: extracted_records extracted_records_submission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracted_records
    ADD CONSTRAINT extracted_records_submission_id_fkey FOREIGN KEY (submission_id) REFERENCES public.submissions(id);


--
-- Name: field_configs field_configs_form_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field_configs
    ADD CONSTRAINT field_configs_form_type_id_fkey FOREIGN KEY (form_type_id) REFERENCES public.form_types(id);


--
-- Name: flexo_printing_records flexo_printing_records_extracted_record_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.flexo_printing_records
    ADD CONSTRAINT flexo_printing_records_extracted_record_id_fkey FOREIGN KEY (extracted_record_id) REFERENCES public.extracted_records(id);


--
-- Name: gravure_printing_records gravure_printing_records_extracted_record_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gravure_printing_records
    ADD CONSTRAINT gravure_printing_records_extracted_record_id_fkey FOREIGN KEY (extracted_record_id) REFERENCES public.extracted_records(id);


--
-- PostgreSQL database dump complete
--

\unrestrict zzMfIBFygmiwZZuCapfa4kTKFYhSEQiSggYYfBzJ3OfHdlihmq23UOpDgoHzja5

