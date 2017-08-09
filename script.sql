-- Создание таблицы decoded_packets
CREATE TABLE public.decoded_packets
(
  id integer NOT NULL DEFAULT nextval('raw_packets_id_seq'::regclass), -- id
  device_id bigint NOT NULL, -- device IMEI
  data text NOT NULL, -- decoded packet
  "timestamp" timestamp with time zone NOT NULL DEFAULT now_ast(), -- date,time when packet has been received
  processed boolean NOT NULL DEFAULT false,
  CONSTRAINT "DPK_ID" PRIMARY KEY (id),
  CONSTRAINT "FK_IMEI" FOREIGN KEY (device_id)
      REFERENCES public.devices (imei) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.decoded_packets
  OWNER TO postgres;
COMMENT ON TABLE public.decoded_packets
  IS 'Разобранные пакеты телеметрии';
COMMENT ON COLUMN public.decoded_packets.id IS 'id';
COMMENT ON COLUMN public.decoded_packets.device_id IS 'device IMEI';
COMMENT ON COLUMN public.decoded_packets.data IS 'decoded packet';
COMMENT ON COLUMN public.decoded_packets."timestamp" IS 'date,time when packet recieved';

-- Создание последовательности для приемников
CREATE SEQUENCE public.receiver_seq
  INCREMENT 1
  MINVALUE 0
  MAXVALUE 9223372036854775807
  START 13
  CACHE 1;
ALTER TABLE public.receiver_seq
  OWNER TO postgres;


-- Создание таблицы приемники
CREATE TABLE public.receivers
(
  id integer NOT NULL DEFAULT nextval('receiver_seq'::regclass), -- id
  name text NOT NULL, -- receiver's name
  address text NOT NULL, -- receiver's address
  port integer NOT NULL, -- receiver's port
  CONSTRAINT "RPK_ID" PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.receivers
  OWNER TO postgres;
COMMENT ON TABLE public.receivers
  IS 'Receivers';
COMMENT ON COLUMN public.receivers.id IS 'id';
COMMENT ON COLUMN public.receivers.name IS 'receivers name';
COMMENT ON COLUMN public.receivers.address IS 'receivers address';
COMMENT ON COLUMN public.receivers.name IS 'receivers port';

-- Функция - Add Receiver
-- Function: public.receiver_add(bigint)
CREATE OR REPLACE FUNCTION public.receiver_add(name text, address text, port text)
  RETURNS bigint AS
$BODY$DECLARE
  clone_count int;
  id_ret int;
BEGIN
  clone_count := 0;
  id_ret := -1;
  EXECUTE 'SELECT count(*) from "receivers" where address = $1' INTO clone_count USING address;
  IF clone_count = 0 THEN
    EXECUTE 'INSERT INTO "receivers" values(DEFAULT, $1, $2, $3) RETURNING id' INTO id_ret USING name, address, port;
    RETURN id_ret;
  ELSE
    RETURN id_ret;
  END IF;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.receiver_add(text, bigint)
  OWNER TO postgres;


-- Table: public.device_receiver
-- Таблица многие ко многим для хранения приборов и приемников к ним;
CREATE TABLE public.device_receiver
(
  device_id bigint,
  receiver_id bigint,
  CONSTRAINT "DEVICE_FOREIGN_KEY" FOREIGN KEY (device_id)
      REFERENCES public.devices (imei) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "RECEIVER_FOREIGN_KEY" FOREIGN KEY (receiver_id)
      REFERENCES public.receivers (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.device_receiver
  OWNER TO postgres;



