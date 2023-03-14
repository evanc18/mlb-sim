__author__ = "Evan Chase"

import pybaseball as pb
import itertools
import contextlib
import sqlite3 as sql
import time

STMT_CREATE_TABLE = """\
    CREATE TABLE IF NOT EXISTS statcast (
                            pitch_type TEXT,
                            game_date TEXT, 
                            release_speed REAL,
                            release_pos_x REAL,
                            release_pos_z REAL,
                            player_name TEXT,
                            batter INT,
                            pitcher INT,
                            events TEXT,
                            description TEXT,
                            spin_dir BLOB,
                            spin_rate_deprecated REAL,
                            break_angle_deprecated REAL,
                            break_length_deprecated REAL,
                            zone INT,
                            des TEXT,
                            game_type TEXT,
                            stand TEXT,
                            p_throws TEXT,
                            home_team TEXT,
                            away_team TEXT,
                            type TEXT,
                            hit_location INT,
                            bb_type TEXT,
                            balls INT,
                            strikes INT,
                            game_year INT,
                            pfx_x REAL,
                            pfx_z REAL,
                            plate_x REAL,
                            plate_z REAL,
                            on_3b INT,
                            on_2b INT,
                            on_1b INT,
                            outs_when_up INT,
                            inning INT,
                            inning_topbot TEXT,
                            hc_x REAL,
                            hc_y REAL,
                            tfs_deprecated BLOB,
                            tfs_zulu_deprecated BLOB,
                            fielder_2 INT,
                            umpire BLOB,
                            sv_id BLOB,
                            vx0 REAL,
                            vy0 REAL,
                            vz0 REAL,
                            ax REAL,
                            ay REAL,
                            az REAL,
                            sz_top REAL,
                            sz_bot REAL,
                            hit_distance_sc INT,
                            launch_speed REAL,
                            launch_angle REAL,
                            effective_speed REAL,
                            release_spin_rate REAL,
                            release_extension REAL,
                            game_pk INT,
                            pitcher_1 INT,
                            fielder_2_1 INT,
                            fielder_3 INT,
                            fielder_4 INT,
                            fielder_5 INT,
                            fielder_6 INT,
                            fielder_7 INT,
                            fielder_8 INT,
                            fielder_9 INT,
                            release_pos_y REAL,
                            estimated_ba_using_speedangle REAL,
                            estimated_woba_using_speedangle REAL,
                            woba_value REAL,
                            woba_denom REAL,
                            babip_value REAL,
                            iso_value REAL,
                            launch_speed_angle REAL,
                            at_bat_number INT,
                            pitch_number INT,
                            pitch_name TEXT,
                            home_score INT,
                            away_score INT,
                            bat_score INT,
                            fld_score INT,
                            post_away_score INT,
                            post_home_score INT,
                            post_bat_score INT,
                            post_fld_score INT,
                            if_fielding_alignment TEXT,
                            of_fielding_alignment TEXT,
                            days_since_2000 INT,
                            PRIMARY KEY (game_pk, at_bat_number, pitch_number));)"""
STMT_INSERT_STCST = """\
    INSERT INTO statcast (
                            pitch_type,
                            game_date,
                            release_speed,
                            release_pos_x,
                            release_pos_z,
                            player_name,
                            batter,
                            pitcher,
                            events,
                            description,
                            spin_dir,
                            spin_rate_deprecated,
                            break_angle_deprecated,
                            break_length_deprecated,
                            zone,
                            des,
                            game_type,
                            stand,
                            p_throws,
                            home_team,
                            away_team,
                            type,
                            hit_location,
                            bb_type,
                            balls,
                            strikes,
                            game_year,
                            pfx_x,
                            pfx_z,
                            plate_x,
                            plate_z,
                            on_3b,
                            on_2b,
                            on_1b,
                            outs_when_up,
                            inning,
                            inning_topbot,
                            hc_x,
                            hc_y,
                            tfs_deprecated,
                            tfs_zulu_deprecated,
                            fielder_2,
                            umpire,
                            sv_id,
                            vx0,
                            vy0,
                            vz0,
                            ax,
                            ay,
                            az,
                            sz_top,
                            sz_bot,
                            hit_distance_sc,
                            launch_speed,
                            launch_angle,
                            effective_speed,
                            release_spin_rate,
                            release_extension,
                            game_pk,
                            pitcher_1,
                            fielder_2_1,
                            fielder_3,
                            fielder_4,
                            fielder_5,
                            fielder_6,
                            fielder_7,
                            fielder_8,
                            fielder_9,
                            release_pos_y,
                            estimated_ba_using_speedangle,
                            estimated_woba_using_speedangle,
                            woba_value,
                            woba_denom,
                            babip_value,
                            iso_value,
                            launch_speed_angle,
                            at_bat_number,
                            pitch_number,
                            pitch_name,
                            home_score,
                            away_score,
                            bat_score,
                            fld_score,
                            post_away_score,
                            post_home_score,
                            post_bat_score,
                            post_fld_score,
                            if_fielding_alignment,
                            of_fielding_alignment, 
                            days_since_2000)
                            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,julianday(?) - julianday(?))"""


class SQLGnome:
    def __init__(self, q, db_path, conn=None, ins_size=100):
        self.q = q
        self.db_path = db_path
        self.conn = conn
        self.ins_size = ins_size

    def connect_db(self):
        """Connects to SQLite database

        Returns:
                bool: connection success
        """
        success = False
        try:
            self.conn = sql.connect(self.db_path)
            success = True
        except Exception as e:
            print(f"Fatal: SQL Database failed to connect! '{e}'")

        return success

    def execute_query(self, q_string):
        """Executes a sql query

        Args:
            q_string (str): Query string

        Returns:
            _type_: _description_
        """
        success = False
        try:
            c = self.conn.cursor()
            c.execute(q_string)
            success = True
        except Exception as e:
            print(f"Error in execution of query: '{e}")
        return success

    def insert_items_from_q(self):
        self.conn = self.connect_db()
        cur = self.conn.cursor()
        inserted = 0
        time.sleep(10)

        while True:
            if self.q.empty():
                time.sleep(3)
            else:
                data_in = self.q.get()

    def insert(self, cur, q_string, item):
        try:
            cur.execute(q_string, item)
            cur.commit()
            return True
        except Error as e:
            print("Could not insert \n{}".format(item))
            print("\t Error: {}".format(e))
            return False
                
