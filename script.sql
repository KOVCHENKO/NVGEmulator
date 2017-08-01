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