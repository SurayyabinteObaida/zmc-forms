--
-- PostgreSQL database dump
--

\restrict XLraBB03ItOeoYDhUiODFmfGYy5dqm56Ws9hnWfuFfigOj2mjf4g64a5QUY94uj

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
35	15	1	flexo_7.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\3ea748a1-a742-48d5-833e-3049a779164b\\flexo_7.jpeg	{"date": "4/3/26", "job_name": "Lezaar Veloor", "job_code": "F-2602-3051", "operator": "Junaid", "supplier": "ZMC", "order_qty": 331, "web_size": "24\\"", "tube_sheet": "Sheet", "bag_size": "8 x 11 x 7", "setting_time": "0:10", "start_time": "9:00", "end_time": "9:30", "core_wt": 33.6, "net_wt": 33.4, "printed_waste": null, "plain_waste": null}	{"date": "4/3/26", "job_name": "Lezaar Veloor", "job_code": "F-2602-3051", "operator": "Junaid", "supplier": "ZMC", "order_qty": "331", "web_size": "24\\"", "tube_sheet": "Sheet", "bag_size": "8 x 11 x 7", "setting_time": "0:10", "start_time": "9:00", "end_time": "9:30", "core_wt": "33.6", "net_wt": "33.4", "printed_waste": null, "plain_waste": null}	saved	\N	0.9	2026-03-24 21:20:10.803607	2026-03-24 21:28:52.078294
36	15	1	flexo_8.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\3ea748a1-a742-48d5-833e-3049a779164b\\flexo_8.jpeg	{"date": "28/12/26", "job_name": "Fashion Week", "job_code": "F-2602-3017", "operator": "Rizwan", "supplier": "ZMC", "order_qty": 150, "web_size": "40", "tube_sheet": "Sheet", "bag_size": "17 x 28", "setting_time": "0:30", "start_time": "15:35", "end_time": "17:00", "core_wt": null, "net_wt": null, "printed_waste": 0.9, "plain_waste": 0.2}	{"date": "28/12/26", "job_name": "Fashion Week", "job_code": "F-2602-3017", "operator": "Rizwan", "supplier": "ZMC", "order_qty": "150", "web_size": "40", "tube_sheet": "Sheet", "bag_size": "17 x 28", "setting_time": "0:30", "start_time": "15:35", "end_time": "17:00", "core_wt": null, "net_wt": null, "printed_waste": "0.9", "plain_waste": "0.2"}	saved	\N	0.9	2026-03-24 21:20:21.548513	2026-03-24 21:28:52.085722
42	17	1	flexo_3.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\c120afc7-16a0-4301-b183-820e07466e7f\\flexo_3.jpeg	{"date": "4/3/2026", "job_name": "Polka Dot", "job_code": "F-2602-3053", "operator": null, "supplier": "ZMC", "order_qty": 140, "web_size": "34", "tube_sheet": "Sheet", "bag_size": "12 x 16 x 2", "setting_time": "0:15", "start_time": "8:45", "end_time": "9:40", "core_wt": 2.1, "net_wt": 140.7, "printed_waste": 0, "plain_waste": 0}	{"date": "4/3/2026", "job_name": "Polka Dot", "job_code": "F-2602-3053", "operator": null, "supplier": "ZMC", "order_qty": "140", "web_size": "34", "tube_sheet": "Sheet", "bag_size": "12 x 16 x 2", "setting_time": "0:15", "start_time": "8:45", "end_time": "9:40", "core_wt": "2.1", "net_wt": "140.7", "printed_waste": null, "plain_waste": null}	saved	\N	1	2026-03-25 17:12:15.395664	2026-03-25 19:46:54.824575
43	17	1	flexo_4.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\c120afc7-16a0-4301-b183-820e07466e7f\\flexo_4.jpeg	{"date": "28/12/2026", "job_name": "RALVIL TEN", "job_code": "F-2602-3041", "operator": "Rizwan", "supplier": "NOVATEX", "order_qty": 72, "web_size": "36.5", "tube_sheet": "Sheet", "bag_size": "12 x 36", "setting_time": "0:25", "start_time": "18:00", "end_time": "21:40", "core_wt": null, "net_wt": 77.8, "printed_waste": 0.2, "plain_waste": 0.3}	{"date": "28/12/2026", "job_name": "RALVIL TEN", "job_code": "F-2602-3041", "operator": "Rizwan", "supplier": "NOVATEX", "order_qty": "72", "web_size": "36.5", "tube_sheet": "Sheet", "bag_size": "12 x 36", "setting_time": "0:25", "start_time": "18:00", "end_time": "21:40", "core_wt": null, "net_wt": "77.8", "printed_waste": "0.2", "plain_waste": "0.3"}	saved	\N	1	2026-03-25 17:12:23.49991	2026-03-25 19:46:54.83846
44	17	1	flexo_5.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\c120afc7-16a0-4301-b183-820e07466e7f\\flexo_5.jpeg	{"date": "6/3/26", "job_name": "MOHSIN RASHID", "job_code": "2703/2703", "operator": "Junaid", "supplier": "ZMC", "order_qty": 850, "web_size": "50x80", "tube_sheet": "Tube", "bag_size": "8x16", "setting_time": "0:35", "start_time": "9:00", "end_time": "13:00", "core_wt": 4.6, "net_wt": 339.3, "printed_waste": 0, "plain_waste": 4.0}	{"date": "6/3/26", "job_name": "MOHSIN RASHID", "job_code": "2703/2703", "operator": "Junaid", "supplier": "ZMC", "order_qty": "850", "web_size": "50x80", "tube_sheet": "Tube", "bag_size": "8x16", "setting_time": "0:35", "start_time": "9:00", "end_time": "13:00", "core_wt": "4.6", "net_wt": "339.3", "printed_waste": null, "plain_waste": "4.0"}	saved	\N	0.95	2026-03-25 17:12:33.007463	2026-03-25 19:46:54.85072
51	22	1	flexo_8.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\705269ba-9057-4f37-a756-5a4f7b173fb1\\flexo_8.jpeg	{"date": "28/12/2026", "job_name": "Fashion Week", "job_code": "F-2602-3017", "operator": "Rizwan", "supplier": "ZMC", "order_qty": 150, "web_size": "40", "tube_sheet": "Sheet", "bag_size": "12x28", "setting_time": "0:30", "start_time": "15:35", "end_time": "17:00", "core_wt": null, "net_wt": 162.56, "printed_waste": 0.9, "plain_waste": 0.2}	\N	extracted	\N	1	2026-03-25 23:52:25.183548	\N
55	24	1	flexo_4.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\00c17e04-06bb-4f04-894e-994964d850ef\\flexo_4.jpeg	{"date": "28/12/2026", "job_name": "Ralvil Ten", "job_code": "F-2602-3044", "operator": "Rizwan", "supplier": "novatex", "order_qty": 72, "web_size": "36.5", "tube_sheet": "Sheet", "bag_size": "12 x 36", "setting_time": "0:25", "start_time": "18:00", "end_time": "21:40", "core_wt": null, "net_wt": 77.8, "printed_waste": 0.2, "plain_waste": 0.3}	\N	extracted	\N	1	2026-03-26 00:34:24.47864	\N
56	24	1	flexo_5.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\00c17e04-06bb-4f04-894e-994964d850ef\\flexo_5.jpeg	{"date": "6/3/26", "job_name": "Mohtam Rash", "job_code": "1-2603-2603", "operator": null, "supplier": "ZMC", "order_qty": 850, "web_size": "20", "tube_sheet": "Tube", "bag_size": "8x16", "setting_time": "0:45", "start_time": "9:00", "end_time": "13:00", "core_wt": 4.6, "net_wt": 344.8, "printed_waste": 0, "plain_waste": 4.0}	\N	extracted	\N	0.9	2026-03-26 00:34:35.117509	\N
57	24	1	flexo_6.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\00c17e04-06bb-4f04-894e-994964d850ef\\flexo_6.jpeg	{"date": "4/3/26", "job_name": "Body & Blast", "job_code": "F-2602-3012", "operator": "Junaid", "supplier": "ZMC", "order_qty": 50, "web_size": "26", "tube_sheet": "Sheet", "bag_size": "11 X 19X2", "setting_time": "0:10", "start_time": "13:00", "end_time": "13:30", "core_wt": 50.8, "net_wt": 51.0, "printed_waste": 0, "plain_waste": 0}	\N	extracted	\N	1	2026-03-26 00:34:44.246486	\N
58	25	1	flexo_7.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\e5784a7c-4be9-4a15-9764-8f7d8e808f7c\\flexo_7.jpeg	{"date": "4/3/26", "job_name": "LEZAAR VELOUR 8X11X2", "job_code": "F-2602-3051", "operator": "Junaid", "supplier": "ZMC", "order_qty": 337, "web_size": "24\\"", "tube_sheet": "Sheet", "bag_size": "8 x 11 x 17", "setting_time": "0:10", "start_time": "9:00", "end_time": "9:30", "core_wt": 1.3, "net_wt": 33.6, "printed_waste": 0, "plain_waste": 0}	\N	extracted	\N	0.95	2026-03-26 00:38:53.7767	\N
59	26	1	flexo_8.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\03f7c6c8-be55-4454-a66a-a5cc5c94a822\\flexo_8.jpeg	{"date": "28/12/2026", "job_name": "FASHION WEEK 17X20", "job_code": "F-2602-3017", "operator": "Rizwan", "supplier": "ZMC", "order_qty": 150, "web_size": "40", "tube_sheet": "Sheet", "bag_size": "17x28", "setting_time": "0:30", "start_time": "15:35", "end_time": "17:00", "core_wt": null, "net_wt": 162.56, "printed_waste": 0.9, "plain_waste": 0.2}	\N	extracted	\N	0.9	2026-03-26 00:39:23.062897	\N
39	16	1	flexo_8.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\6d7925e6-c869-4fd2-995f-858709cd9c8b\\flexo_8.jpeg	{"date": "28/12/26", "job_name": "Fashion Week", "job_code": "F-2602-3017", "operator": "Rizwan", "supplier": "ZMC", "order_qty": 150, "web_size": "40", "tube_sheet": "Sheet", "bag_size": "17x28", "setting_time": "0:30", "start_time": "15:35", "end_time": "17:00", "core_wt": 163.1, "net_wt": 162.86, "printed_waste": 0.7, "plain_waste": 0.2}	{"date": "28/12/26", "job_name": "Fashion Week", "job_code": "F-2602-3017", "operator": "Rizwan", "supplier": "ZMC", "order_qty": "150", "web_size": "40", "tube_sheet": "Sheet", "bag_size": "17x28", "setting_time": "0:30", "start_time": "15:35", "end_time": "17:00", "core_wt": "163.1", "net_wt": "162.86", "printed_waste": "0.7", "plain_waste": "0.2"}	saved	\N	1	2026-03-25 16:02:21.009353	2026-03-25 17:10:59.132205
40	17	1	flexo_1.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\c120afc7-16a0-4301-b183-820e07466e7f\\flexo_1.jpeg	{"date": "4/3/2026", "job_name": "Polka Dot Solve to get 5% Discount", "job_code": "F-2608-3052", "operator": "Junaid", "supplier": "ZMC", "order_qty": 40, "web_size": "24", "tube_sheet": "Sheet", "bag_size": "10 x 11 x 2 Pocket", "setting_time": "0:05", "start_time": "13:45", "end_time": "14:00", "core_wt": null, "net_wt": 41.16, "printed_waste": 0, "plain_waste": 0.5}	{"date": "4/3/2026", "job_name": "Polka Dot Solve to get 5% Discount", "job_code": "F-2608-3052", "operator": "Junaid", "supplier": "ZMC", "order_qty": "40", "web_size": "24", "tube_sheet": "Sheet", "bag_size": "10 x 11 x 2 Pocket", "setting_time": "0:05", "start_time": "13:45", "end_time": "14:00", "core_wt": null, "net_wt": "41.16", "printed_waste": null, "plain_waste": "0.5"}	saved	\N	1	2026-03-25 17:11:55.452082	2026-03-25 19:46:54.733908
38	16	1	flexo_7.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\6d7925e6-c869-4fd2-995f-858709cd9c8b\\flexo_7.jpeg	{"date": "4/3/26", "job_name": "Lezaar Veloor", "job_code": "F-2602-3051", "operator": "Junaid", "supplier": "7nuc", "order_qty": 331, "web_size": "24\\"", "tube_sheet": "Sheet", "bag_size": "8x11+2", "setting_time": "0:10", "start_time": "9:00", "end_time": "9:30", "core_wt": 33.4, "net_wt": 33.6, "printed_waste": null, "plain_waste": null}	{"date": "4/3/26", "job_name": "Lezaar Veloor", "job_code": "F-2602-3051", "operator": "Junaid", "supplier": "7nuc", "order_qty": "331", "web_size": "24\\"", "tube_sheet": "Sheet", "bag_size": "8x11+2", "setting_time": "0:10", "start_time": "9:00", "end_time": "9:30", "core_wt": "33.4", "net_wt": "33.6", "printed_waste": null, "plain_waste": null}	saved	\N	1	2026-03-25 16:02:13.4289	2026-03-25 17:10:55.289586
41	17	1	flexo_2.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\c120afc7-16a0-4301-b183-820e07466e7f\\flexo_2.jpeg	{"date": "2/3/2026", "job_name": "Raja Fashion (Black + Silver + Blue + Yellow)", "job_code": "F-2602-3047", "operator": "Junaid", "supplier": "N/A", "order_qty": 66, "web_size": "27", "tube_sheet": "Sheet", "bag_size": "11 X 36", "setting_time": "0:30", "start_time": "17:30", "end_time": "22:25", "core_wt": null, "net_wt": 73.1, "printed_waste": 0.1, "plain_waste": 0.5}	{"date": "2/3/2026", "job_name": "Raja Fashion (Black + Silver + Blue + Yellow)", "job_code": "F-2602-3047", "operator": "Junaid", "supplier": "N/A", "order_qty": "66", "web_size": "27", "tube_sheet": "Sheet", "bag_size": "11 X 36", "setting_time": "0:30", "start_time": "17:30", "end_time": "22:25", "core_wt": null, "net_wt": "73.1", "printed_waste": "0.1", "plain_waste": "0.5"}	saved	\N	0.95	2026-03-25 17:12:04.834189	2026-03-25 19:46:54.811093
45	17	1	flexo_6.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\c120afc7-16a0-4301-b183-820e07466e7f\\flexo_6.jpeg	{"date": "4/3/26", "job_name": "Body & Blast", "job_code": "F-2602-3012", "operator": "Junaid", "supplier": "ZMC", "order_qty": 50, "web_size": "26", "tube_sheet": "Sheet", "bag_size": "11x19x12", "setting_time": "0:10", "start_time": "13:00", "end_time": "13:30", "core_wt": null, "net_wt": 51, "printed_waste": 0, "plain_waste": 0}	{"date": "4/3/26", "job_name": "Body & Blast", "job_code": "F-2602-3012", "operator": "Junaid", "supplier": "ZMC", "order_qty": "50", "web_size": "26", "tube_sheet": "Sheet", "bag_size": "11x19x12", "setting_time": "0:10", "start_time": "13:00", "end_time": "13:30", "core_wt": null, "net_wt": "51", "printed_waste": null, "plain_waste": null}	saved	\N	1	2026-03-25 17:12:41.207736	2026-03-25 19:46:54.861207
46	17	1	flexo_7.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\c120afc7-16a0-4301-b183-820e07466e7f\\flexo_7.jpeg	{"date": "4/3/26", "job_name": "Lezaar Veloor", "job_code": "F-2602-3051", "operator": "Junaid", "supplier": "7 Ind", "order_qty": 331, "web_size": "24\\"", "tube_sheet": "Sheet", "bag_size": "8x11x12", "setting_time": "0:10", "start_time": "9:00", "end_time": "9:30", "core_wt": null, "net_wt": 33.4, "printed_waste": null, "plain_waste": null}	{"date": "4/3/26", "job_name": "Lezaar Veloor", "job_code": "F-2602-3051", "operator": "Junaid", "supplier": "7 Ind", "order_qty": "331", "web_size": "24\\"", "tube_sheet": "Sheet", "bag_size": "8x11x12", "setting_time": "0:10", "start_time": "9:00", "end_time": "9:30", "core_wt": null, "net_wt": "33.4", "printed_waste": null, "plain_waste": null}	saved	\N	0.95	2026-03-25 17:12:48.960736	2026-03-25 19:46:54.871004
47	17	1	flexo_8.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\c120afc7-16a0-4301-b183-820e07466e7f\\flexo_8.jpeg	{"date": "28/12/2026", "job_name": "Fashion Week", "job_code": "F-2602-3017", "operator": "Rizwan", "supplier": "ZMC", "order_qty": 150, "web_size": "40", "tube_sheet": "Sheet", "bag_size": "17x28", "setting_time": "0:30", "start_time": "15:35", "end_time": "17:00", "core_wt": null, "net_wt": 162.56, "printed_waste": 0.7, "plain_waste": 3.2}	{"date": "28/12/2026", "job_name": "Fashion Week", "job_code": "F-2602-3017", "operator": "Rizwan", "supplier": "ZMC", "order_qty": "150", "web_size": "40", "tube_sheet": "Sheet", "bag_size": "17x28", "setting_time": "0:30", "start_time": "15:35", "end_time": "17:00", "core_wt": null, "net_wt": "162.56", "printed_waste": "0.7", "plain_waste": "3.2"}	saved	\N	1	2026-03-25 17:12:58.323992	2026-03-25 19:46:54.880957
52	23	1	flexo_6.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\054579ea-c3a8-4ca1-8dd3-f6dcdd07d7f2\\flexo_6.jpeg	{"date": "4/3/26", "job_name": "Body & Blast", "job_code": "F-2602-3012", "operator": "Junaid", "supplier": "ZMC", "order_qty": 50, "web_size": "26", "tube_sheet": "Sheet", "bag_size": "11 X 19 X 2", "setting_time": "0:10", "start_time": "13:00", "end_time": "13:30", "core_wt": null, "net_wt": 51.0, "printed_waste": null, "plain_waste": null}	\N	extracted	\N	1	2026-03-26 00:21:54.683765	\N
53	23	1	flexo_7.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\054579ea-c3a8-4ca1-8dd3-f6dcdd07d7f2\\flexo_7.jpeg	{"date": "4/3/26", "job_name": "LEZAAR VELOOR", "job_code": "F-2602-3051", "operator": "Junaid", "supplier": "Indc", "order_qty": 331, "web_size": "24\\"", "tube_sheet": "Sheet", "bag_size": "8x11x17", "setting_time": "0:10", "start_time": "9:00", "end_time": "9:30", "core_wt": null, "net_wt": 33.4, "printed_waste": null, "plain_waste": null}	\N	extracted	\N	0.95	2026-03-26 00:22:03.001193	\N
54	23	1	flexo_8.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\054579ea-c3a8-4ca1-8dd3-f6dcdd07d7f2\\flexo_8.jpeg	{"date": "28/12/2026", "job_name": "Fashion Week", "job_code": "F-2602-3017", "operator": "Rizwan", "supplier": "ZMC", "order_qty": 150, "web_size": "40", "tube_sheet": "Sheet", "bag_size": "17x20", "setting_time": "0:30", "start_time": "15:35", "end_time": "17:00", "core_wt": null, "net_wt": 163.1, "printed_waste": 0.9, "plain_waste": 0.2}	\N	extracted	\N	1	2026-03-26 00:22:11.846549	\N
29	15	1	flexo_1.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\3ea748a1-a742-48d5-833e-3049a779164b\\flexo_1.jpeg	{"date": "4/3/26", "job_name": "Polka Dot Solve to get 5% Discount", "job_code": "F-2602-3052", "operator": "Junaid", "supplier": "ZMC", "order_qty": 40, "web_size": "24", "tube_sheet": "Sheet", "bag_size": "10x11.2 Pocket", "setting_time": "0:15", "start_time": "13:45", "end_time": "14:00", "core_wt": 56.0, "net_wt": 41.16, "printed_waste": null, "plain_waste": 0.5}	{"date": "4/3/26", "job_name": "Polka Dot Solve to get 5% Discount", "job_code": "F-2602-3052", "operator": "Junaid", "supplier": "ZMC", "order_qty": "40", "web_size": "24", "tube_sheet": "Sheet", "bag_size": "10x11.2 Pocket", "setting_time": "0:15", "start_time": "13:45", "end_time": "14:00", "core_wt": "56.0", "net_wt": "41.16", "printed_waste": null, "plain_waste": "0.5"}	saved	\N	1	2026-03-24 21:19:21.610446	2026-03-24 21:25:07.637853
30	15	1	flexo_2.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\3ea748a1-a742-48d5-833e-3049a779164b\\flexo_2.jpeg	{"date": "2/3/26", "job_name": "Raja Fashion (Black + Silver + Blue + Yellow)", "job_code": "F-2602-3042", "operator": "Junaid", "supplier": "N/A", "order_qty": 66, "web_size": "27", "tube_sheet": "Sheet", "bag_size": "11 X 36", "setting_time": "0:30", "start_time": "17:30", "end_time": "22:25", "core_wt": 84, "net_wt": 78.3, "printed_waste": 0.1, "plain_waste": 0.5}	{"date": "2/3/26", "job_name": "Raja Fashion (Black + Silver + Blue + Yellow)", "job_code": "F-2602-3042", "operator": "Junaid", "supplier": "N/A", "order_qty": "66", "web_size": "27", "tube_sheet": "Sheet", "bag_size": "11 X 36", "setting_time": "0:30", "start_time": "17:30", "end_time": "22:25", "core_wt": "84", "net_wt": "78.3", "printed_waste": "0.1", "plain_waste": "0.5"}	saved	\N	1	2026-03-24 21:19:29.318489	2026-03-24 21:27:02.393893
31	15	1	flexo_3.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\3ea748a1-a742-48d5-833e-3049a779164b\\flexo_3.jpeg	{"date": "4/3/26", "job_name": "Polka Dot", "job_code": "F-2602-3053", "operator": "Raymond", "supplier": "ZMC", "order_qty": 140, "web_size": "34", "tube_sheet": "Sheet", "bag_size": "12 X 16 X 2", "setting_time": "0:15", "start_time": "8:45", "end_time": "9:40", "core_wt": 2.1, "net_wt": 141.8, "printed_waste": null, "plain_waste": null}	{"date": "4/3/26", "job_name": "Polka Dot", "job_code": "F-2602-3053", "operator": "Raymond", "supplier": "ZMC", "order_qty": "140", "web_size": "34", "tube_sheet": "Sheet", "bag_size": "12 X 16 X 2", "setting_time": "0:15", "start_time": "8:45", "end_time": "9:40", "core_wt": "2.1", "net_wt": "141.8", "printed_waste": null, "plain_waste": null}	saved	\N	1	2026-03-24 21:19:36.184204	2026-03-24 21:28:18.574521
32	15	1	flexo_4.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\3ea748a1-a742-48d5-833e-3049a779164b\\flexo_4.jpeg	{"date": "28/12/26", "job_name": "Ralvil Ten", "job_code": "F-2602-3044", "operator": "Rizwan", "supplier": "Novatex", "order_qty": 72, "web_size": "36.5", "tube_sheet": "Sheet", "bag_size": "12 x 36", "setting_time": "0:25", "start_time": "18:00", "end_time": "21:40", "core_wt": null, "net_wt": 89.1, "printed_waste": 0.2, "plain_waste": 0.3}	{"date": "28/12/26", "job_name": "Ralvil Ten", "job_code": "F-2602-3044", "operator": "Rizwan", "supplier": "Novatex", "order_qty": "72", "web_size": "36.5", "tube_sheet": "Sheet", "bag_size": "12 x 36", "setting_time": "0:25", "start_time": "18:00", "end_time": "21:40", "core_wt": null, "net_wt": "89.1", "printed_waste": "0.2", "plain_waste": "0.3"}	saved	\N	1	2026-03-24 21:19:43.355334	2026-03-24 21:28:52.046968
33	15	1	flexo_5.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\3ea748a1-a742-48d5-833e-3049a779164b\\flexo_5.jpeg	{"date": "6/3/2026", "job_name": "MOHSIN RASHID", "job_code": "1-7603/7603", "operator": "Junaid", "supplier": "ZMC", "order_qty": 850, "web_size": "4kg", "tube_sheet": "Tube", "bag_size": "8x16", "setting_time": "0:15", "start_time": "9:00", "end_time": "13:00", "core_wt": 4.6, "net_wt": 313.0, "printed_waste": null, "plain_waste": 4.0}	{"date": "6/3/2026", "job_name": "MOHSIN RASHID", "job_code": "1-7603/7603", "operator": "Junaid", "supplier": "ZMC", "order_qty": "850", "web_size": "4kg", "tube_sheet": "Tube", "bag_size": "8x16", "setting_time": "0:15", "start_time": "9:00", "end_time": "13:00", "core_wt": "4.6", "net_wt": "313.0", "printed_waste": null, "plain_waste": "4.0"}	saved	\N	1	2026-03-24 21:19:52.775008	2026-03-24 21:28:52.057989
34	15	1	flexo_6.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\3ea748a1-a742-48d5-833e-3049a779164b\\flexo_6.jpeg	{"date": "4/3/26", "job_name": "Body & Blast", "job_code": "F-2602-3012", "operator": "Junaid", "supplier": "ZMC", "order_qty": 50, "web_size": "26", "tube_sheet": "Sheet", "bag_size": "11 X 15 1/2", "setting_time": "0:10", "start_time": "13:00", "end_time": "13:30", "core_wt": 101.0, "net_wt": 52.4, "printed_waste": null, "plain_waste": null}	{"date": "4/3/26", "job_name": "Body & Blast", "job_code": "F-2602-3012", "operator": "Junaid", "supplier": "ZMC", "order_qty": "50", "web_size": "26", "tube_sheet": "Sheet", "bag_size": "11 X 15 1/2", "setting_time": "0:10", "start_time": "13:00", "end_time": "13:30", "core_wt": "101.0", "net_wt": "52.4", "printed_waste": null, "plain_waste": null}	saved	\N	1	2026-03-24 21:20:00.147513	2026-03-24 21:28:52.070619
37	16	1	flexo_6.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\6d7925e6-c869-4fd2-995f-858709cd9c8b\\flexo_6.jpeg	{"date": "4/3/26", "job_name": "Body & Blast", "job_code": "F-2602-3012", "operator": "Junaid", "supplier": "ZMC", "order_qty": 50, "web_size": "26", "tube_sheet": "Sheet", "bag_size": "11 x 19 x 2", "setting_time": "0:10", "start_time": "13:00", "end_time": "13:30", "core_wt": 50.8, "net_wt": 51.0, "printed_waste": null, "plain_waste": null}	{"date": "4/3/26", "job_name": "Body & Blast", "job_code": "F-2602-3012", "operator": "Junaid", "supplier": "ZMC", "order_qty": "50", "web_size": "26", "tube_sheet": "Sheet", "bag_size": "11 x 19 x 2", "setting_time": "0:10", "start_time": "13:00", "end_time": "13:30", "core_wt": "50.8", "net_wt": "51.0", "printed_waste": null, "plain_waste": null}	saved	\N	1	2026-03-25 16:02:04.795681	2026-03-25 17:10:59.125317
49	22	1	flexo_6.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\705269ba-9057-4f37-a756-5a4f7b173fb1\\flexo_6.jpeg	{"date": "4/3/26", "job_name": "Body & Blast", "job_code": "F-2602-3012", "operator": "Junaid", "supplier": "ZMC", "order_qty": 50, "web_size": "26", "tube_sheet": "Sheet", "bag_size": "11 X 19572", "setting_time": "0:10", "start_time": "13:00", "end_time": "13:30", "core_wt": 50.8, "net_wt": 51.0, "printed_waste": 0, "plain_waste": 0}	\N	extracted	\N	1	2026-03-25 23:52:05.522154	\N
50	22	1	flexo_7.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\705269ba-9057-4f37-a756-5a4f7b173fb1\\flexo_7.jpeg	{"date": "4/3/26", "job_name": "LEZAAR VELOOR", "job_code": "F-2602-3051", "operator": "Junaid", "supplier": "ZMC", "order_qty": 331, "web_size": "24\\"", "tube_sheet": "Sheet", "bag_size": "8x11+7", "setting_time": "0:10", "start_time": "9:00", "end_time": "9:30", "core_wt": 1.3, "net_wt": 33.4, "printed_waste": 0, "plain_waste": 0}	\N	extracted	\N	1	2026-03-25 23:52:16.121915	\N
60	27	1	flexo_6.jpeg	E:\\Softwares\\xampp\\htdocs\\ZMC\\zmc_forms\\app\\uploads\\a7f34c41-f9db-447a-ae24-ed82eb11c413\\flexo_6.jpeg	{"date": "4/3/26", "job_name": "Body & Blast", "job_code": "F-2602-3012", "operator": "Junaid", "supplier": "ZMC", "order_qty": 50, "web_size": "26", "tube_sheet": "Sheet", "bag_size": "11 X 19/72", "setting_time": "0:10", "start_time": "13:00", "end_time": "13:30", "core_wt": 0, "net_wt": 51.0, "printed_waste": 0, "plain_waste": 0}	\N	extracted	\N	1	2026-03-26 00:39:51.636513	\N
\.


--
-- Data for Name: field_configs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.field_configs (id, form_type_id, key, label, field_type, enabled, "order") FROM stdin;
1	1	date	Date	date	t	1
2	1	job_name	Job Name	text	t	2
3	1	job_code	Job Code	text	t	3
5	1	operator	Operator	text	t	5
17	1	tube_sheet	Tube/Sheet	text	t	17
18	1	bag_size	Bag Size	text	t	18
19	1	setting_time	Setting Time	text	t	19
20	1	start_time	Start Time	text	t	20
21	1	end_time	End Time	text	t	21
35	1	printed_waste	Printed Waste	number	t	35
36	1	plain_waste	Plain Waste	number	t	36
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
4	1	party_name	Party Name	text	f	4
6	1	material	Material	text	f	6
8	1	rm_number	R.M #	text	f	8
11	1	mic	Mic	text	f	11
12	1	cylinder_size	Cylinder Size	text	f	12
13	1	no_of_colors	No. of Colors	number	f	13
14	1	ink_gsm	Ink GSM	number	f	14
15	1	speed	Speed	number	f	15
16	1	block_number	Block #	text	f	16
22	1	plain_roll_wt	Plain Roll Wt.	number	f	22
23	1	plain_bal	Plain Balance	number	f	23
24	1	printed_roll_number	Printed Roll #	text	f	24
25	1	printed_reel_wt	Printed Reel Wt.	number	f	25
27	1	counter_meter	Counter / Meter	text	f	27
28	1	balance_rejected	Balance / Rejected	text	f	28
29	1	gross_wt	Gross Wt.	number	f	29
31	1	total_counter	Total Counter	number	f	31
32	1	total_meter	Total Meter	number	f	32
33	1	setting_waste	Setting Waste	number	f	33
34	1	roll_waste	Roll Waste	number	f	34
37	1	total_waste	Total Waste	number	f	37
38	1	rejected_core_wt	Rejected Core Wt.	number	f	38
39	1	prepared_by	Prepared By	text	f	39
40	1	supervisor	Supervisor	text	f	40
41	1	remarks	Remarks	text	f	41
7	1	supplier	Material Supplier	text	t	7
9	1	order_qty	Order Qty	number	t	9
10	1	web_size	Web Size	text	t	10
26	1	core_wt	Plain Net Wt.	number	t	26
30	1	net_wt	Printed Net Wt.	number	t	30
\.


--
-- Data for Name: flexo_printing_records; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.flexo_printing_records (id, extracted_record_id, saved_at, date, job_name, job_code, party_name, operator, material, supplier, rm_number, order_qty, web_size, mic, cylinder_size, no_of_colors, ink_gsm, speed, block_number, tube_sheet, bag_size, setting_time, start_time, end_time, plain_roll_wt, plain_bal, printed_roll_number, printed_reel_wt, core_wt, counter_meter, balance_rejected, gross_wt, net_wt, total_counter, total_meter, setting_waste, roll_waste, printed_waste, plain_waste, total_waste, rejected_core_wt, prepared_by, supervisor, remarks) FROM stdin;
9	29	2026-03-24 21:25:07.644146	4/3/26	Polka Dot Solve to get 5% Discount	F-2602-3052	\N	Junaid	\N	ZMC	\N	40	24	\N	\N	\N	\N	\N	\N	Sheet	10x11.2 Pocket	0:15	13:45	14:00	\N	\N	\N	\N	56	\N	\N	\N	41.16	\N	\N	\N	\N	\N	0.5	\N	\N	\N	\N	\N
10	30	2026-03-24 21:27:02.399243	2/3/26	Raja Fashion (Black + Silver + Blue + Yellow)	F-2602-3042	\N	Junaid	\N	N/A	\N	66	27	\N	\N	\N	\N	\N	\N	Sheet	11 X 36	0:30	17:30	22:25	\N	\N	\N	\N	84	\N	\N	\N	78.3	\N	\N	\N	\N	0.1	0.5	\N	\N	\N	\N	\N
11	31	2026-03-24 21:28:18.57993	4/3/26	Polka Dot	F-2602-3053	\N	Raymond	\N	ZMC	\N	140	34	\N	\N	\N	\N	\N	\N	Sheet	12 X 16 X 2	0:15	8:45	9:40	\N	\N	\N	\N	2.1	\N	\N	\N	141.8	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
12	32	2026-03-24 21:28:52.054261	28/12/26	Ralvil Ten	F-2602-3044	\N	Rizwan	\N	Novatex	\N	72	36.5	\N	\N	\N	\N	\N	\N	Sheet	12 x 36	0:25	18:00	21:40	\N	\N	\N	\N	\N	\N	\N	\N	89.1	\N	\N	\N	\N	0.2	0.3	\N	\N	\N	\N	\N
13	33	2026-03-24 21:28:52.063583	6/3/2026	MOHSIN RASHID	1-7603/7603	\N	Junaid	\N	ZMC	\N	850	4kg	\N	\N	\N	\N	\N	\N	Tube	8x16	0:15	9:00	13:00	\N	\N	\N	\N	4.6	\N	\N	\N	313	\N	\N	\N	\N	\N	4	\N	\N	\N	\N	\N
14	34	2026-03-24 21:28:52.075821	4/3/26	Body & Blast	F-2602-3012	\N	Junaid	\N	ZMC	\N	50	26	\N	\N	\N	\N	\N	\N	Sheet	11 X 15 1/2	0:10	13:00	13:30	\N	\N	\N	\N	101	\N	\N	\N	52.4	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
15	35	2026-03-24 21:28:52.082966	4/3/26	Lezaar Veloor	F-2602-3051	\N	Junaid	\N	ZMC	\N	331	24"	\N	\N	\N	\N	\N	\N	Sheet	8 x 11 x 7	0:10	9:00	9:30	\N	\N	\N	\N	33.6	\N	\N	\N	33.4	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
16	36	2026-03-24 21:28:52.090627	28/12/26	Fashion Week	F-2602-3017	\N	Rizwan	\N	ZMC	\N	150	40	\N	\N	\N	\N	\N	\N	Sheet	17 x 28	0:30	15:35	17:00	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	0.9	0.2	\N	\N	\N	\N	\N
17	38	2026-03-25 17:10:55.313632	4/3/26	Lezaar Veloor	F-2602-3051	\N	Junaid	\N	7nuc	\N	331	24"	\N	\N	\N	\N	\N	\N	Sheet	8x11+2	0:10	9:00	9:30	\N	\N	\N	\N	33.4	\N	\N	\N	33.6	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
18	37	2026-03-25 17:10:59.129663	4/3/26	Body & Blast	F-2602-3012	\N	Junaid	\N	ZMC	\N	50	26	\N	\N	\N	\N	\N	\N	Sheet	11 x 19 x 2	0:10	13:00	13:30	\N	\N	\N	\N	50.8	\N	\N	\N	51	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
19	39	2026-03-25 17:10:59.137267	28/12/26	Fashion Week	F-2602-3017	\N	Rizwan	\N	ZMC	\N	150	40	\N	\N	\N	\N	\N	\N	Sheet	17x28	0:30	15:35	17:00	\N	\N	\N	\N	163.1	\N	\N	\N	162.86	\N	\N	\N	\N	0.7	0.2	\N	\N	\N	\N	\N
20	40	2026-03-25 19:46:54.787378	4/3/2026	Polka Dot Solve to get 5% Discount	F-2608-3052	\N	Junaid	\N	ZMC	\N	40	24	\N	\N	\N	\N	\N	\N	Sheet	10 x 11 x 2 Pocket	0:05	13:45	14:00	\N	\N	\N	\N	\N	\N	\N	\N	41.16	\N	\N	\N	\N	\N	0.5	\N	\N	\N	\N	\N
21	41	2026-03-25 19:46:54.819621	2/3/2026	Raja Fashion (Black + Silver + Blue + Yellow)	F-2602-3047	\N	Junaid	\N	N/A	\N	66	27	\N	\N	\N	\N	\N	\N	Sheet	11 X 36	0:30	17:30	22:25	\N	\N	\N	\N	\N	\N	\N	\N	73.1	\N	\N	\N	\N	0.1	0.5	\N	\N	\N	\N	\N
22	42	2026-03-25 19:46:54.831678	4/3/2026	Polka Dot	F-2602-3053	\N	\N	\N	ZMC	\N	140	34	\N	\N	\N	\N	\N	\N	Sheet	12 x 16 x 2	0:15	8:45	9:40	\N	\N	\N	\N	2.1	\N	\N	\N	140.7	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
23	43	2026-03-25 19:46:54.845591	28/12/2026	RALVIL TEN	F-2602-3041	\N	Rizwan	\N	NOVATEX	\N	72	36.5	\N	\N	\N	\N	\N	\N	Sheet	12 x 36	0:25	18:00	21:40	\N	\N	\N	\N	\N	\N	\N	\N	77.8	\N	\N	\N	\N	0.2	0.3	\N	\N	\N	\N	\N
24	44	2026-03-25 19:46:54.857479	6/3/26	MOHSIN RASHID	2703/2703	\N	Junaid	\N	ZMC	\N	850	50x80	\N	\N	\N	\N	\N	\N	Tube	8x16	0:35	9:00	13:00	\N	\N	\N	\N	4.6	\N	\N	\N	339.3	\N	\N	\N	\N	\N	4	\N	\N	\N	\N	\N
25	45	2026-03-25 19:46:54.866981	4/3/26	Body & Blast	F-2602-3012	\N	Junaid	\N	ZMC	\N	50	26	\N	\N	\N	\N	\N	\N	Sheet	11x19x12	0:10	13:00	13:30	\N	\N	\N	\N	\N	\N	\N	\N	51	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
26	46	2026-03-25 19:46:54.876971	4/3/26	Lezaar Veloor	F-2602-3051	\N	Junaid	\N	7 Ind	\N	331	24"	\N	\N	\N	\N	\N	\N	Sheet	8x11x12	0:10	9:00	9:30	\N	\N	\N	\N	\N	\N	\N	\N	33.4	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
27	47	2026-03-25 19:46:54.887479	28/12/2026	Fashion Week	F-2602-3017	\N	Rizwan	\N	ZMC	\N	150	40	\N	\N	\N	\N	\N	\N	Sheet	17x28	0:30	15:35	17:00	\N	\N	\N	\N	\N	\N	\N	\N	162.56	\N	\N	\N	\N	0.7	3.2	\N	\N	\N	\N	\N
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
15	3ea748a1-a742-48d5-833e-3049a779164b	2026-03-24 21:19:11.219402	saved
16	6d7925e6-c869-4fd2-995f-858709cd9c8b	2026-03-25 16:01:53.386221	saved
17	c120afc7-16a0-4301-b183-820e07466e7f	2026-03-25 17:11:45.133268	saved
22	705269ba-9057-4f37-a756-5a4f7b173fb1	2026-03-25 23:51:54.946958	extracted
23	054579ea-c3a8-4ca1-8dd3-f6dcdd07d7f2	2026-03-26 00:21:43.262478	extracted
24	00c17e04-06bb-4f04-894e-994964d850ef	2026-03-26 00:34:13.156379	extracted
25	e5784a7c-4be9-4a15-9764-8f7d8e808f7c	2026-03-26 00:38:43.117378	extracted
26	03f7c6c8-be55-4454-a66a-a5cc5c94a822	2026-03-26 00:39:15.938795	extracted
27	a7f34c41-f9db-447a-ae24-ed82eb11c413	2026-03-26 00:39:40.392972	extracted
\.


--
-- Name: extracted_records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.extracted_records_id_seq', 60, true);


--
-- Name: field_configs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.field_configs_id_seq', 78, true);


--
-- Name: flexo_printing_records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.flexo_printing_records_id_seq', 27, true);


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

SELECT pg_catalog.setval('public.submissions_id_seq', 27, true);


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

\unrestrict XLraBB03ItOeoYDhUiODFmfGYy5dqm56Ws9hnWfuFfigOj2mjf4g64a5QUY94uj

