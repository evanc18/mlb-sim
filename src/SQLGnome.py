__author__ = "Evan Chase"

import pybaseball as pb
import itertools
import contextlib
import sqlite3 as sql
import time
from utils.console_log_utils import printProgressBar

"""
All SQL statements for pushing, accessing, etc. Probably will find a better place for these
"""
sql_statements = {
    "statcast": {
       "CREATE": """\
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
                            PRIMARY KEY (game_pk, at_bat_number, pitch_number));""",
       "INSERT": """\
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
                            of_fielding_alignment)
                            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        "DROP": """\
            DROP TABLE IF EXISTS statcast;
        """,
        "PRINT": """\
            SELECT * FROM statcast
        """
    },
    "pitching_stats_range": {
        "CREATE": """\
            CREATE TABLE IF NOT EXISTS pitching_stats_range (
            Name TEXT,
            Age INT,
            Days INT,
            Lev TEXT,
            Tm TEXT,
            G INT,
            GS INT,
            W INT,
            L INT,
            SV INT,
            IP FLOAT,
            H INT,
            R INT,
            ER INT,
            BB INT,
            SO INT,
            HR INT,
            HBP INT,
            ERA FLOAT,
            AB INT,
            Doubles INT,
            Triples INT,
            IBB INT,
            GDP INT,
            SF INT,
            SB INT,
            CS INT,
            PO INT,
            BF INT,
            Pit INT,
            Str FLOAT,
            StL FLOAT,
            StS FLOAT,
            GB_FB FLOAT,
            LD FLOAT,
            PU FLOAT,
            WHIP FLOAT,
            BAbip FLOAT,
            SO9 FLOAT,
            SO_W FLOAT,
            mlbID, INT
            );
            """,
        "INSERT": """\
            INSERT INTO pitching_stats_range (
                Name,
                Age,
                Days,
                Lev,
                Tm,
                G,
                GS,
                W,
                L,
                SV,
                IP,
                H,
                R,
                ER,
                BB,
                SO,
                HR,
                HBP,
                ERA,
                AB,
                Doubles,
                Triples,
                IBB,
                GDP,
                SF,
                SB,
                CS,
                PO,
                BF,
                Pit,
                Str,
                StL,
                StS,
                GB_FB,
                LD,
                PU,
                WHIP,
                BAbip,
                SO9,
                SO_W,
                mlbID)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
        "DROP": """\
            DROP TABLE IF EXISTS pitching_stats_range;
            """,
        "PRINT": """\
            SELECT * FROM pitching_stats_range
            """
    },
    "batting_stats_range": { 
        "CREATE": """\
            CREATE TABLE IF NOT EXISTS batting_stats_range (
                Name TEXT,
                Age INT,
                Days INT,
                Lev TEXT,
                Tm TEXT,
                G INT,
                PA INT,
                AB INT,
                R INT,
                H INT,
                Doubles INT,
                Triples INT,
                HR INT,
                RBI INT,
                BB INT,
                IBB INT,
                SO INT,
                HBP INT,
                SH INT,
                SF INT,
                GDP INT,
                SB INT,
                CS INT,
                BA FLOAT,
                OBP FLOAT,
                SLG FLOAT,
                OPS FLOAT,
                mlbID INT
            );
            """,
        "INSERT": """\
            INSERT INTO batting_stats_range (
                Name,
                Age,
                Days,
                Lev,
                Tm,
                G,
                PA,
                AB,
                R,
                H,
                Doubles,
                Triples,
                HR,
                RBI,
                BB,
                IBB,
                SO,
                HBP,
                SH,
                SF,
                GDP,
                SB,
                CS,
                BA,
                OBP,
                SLG,
                OPS,
                mlbID)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
        "DROP": """\
            DROP TABLE IF EXISTS batting_stats_range;
            """,
        "PRINT": """\
            SELECT * FROM batting_stats_range
            """
    }
}



# TODO STMT_CREATE_STATCAST_PITCHING
# TODO STMT_INSERT_STATCAST_PITCHING
# TODO STMT_DROP_STATCAST_PITCHING
# TODO STMT_PRINT_STATCAST_PITCHING


class SQLGnome:
    def __init__(
        self, q_in, db_path, stop_term, stop_lim, conn=None, ins_size=10000
    ):
        self.q_in = q_in
        self.db_path = db_path
        self.stop_term = stop_term
        self.stop_lim = stop_lim
        self.stop_n = 0
        self.conn = conn
        self.ins_size = ins_size

    def reset_stop_lim(self, lim):
        self.stop_lim = lim
        self.stop_n = 0

    def connect_db(self):
        """Connects to SQLite database

        Returns:
                bool: connection success
        """

        print(
            "Attempting to connect to SQL database: {}".format(self.db_path)
        )
        try:
            self.conn = sql.connect(self.db_path)
            print("Database connection successful!")
            return True
        except Exception as e:
            print(f"Fatal: SQL Database failed to connect! '{e}'")
            return False

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

    def print_table(self, table):
        try:
            c = self.conn.cursor()
            c.execute(table["PRINT"])
            print(c.fetchall())
            success = True
        except Exception as e:
            print(f"Error in execution of query: '{e}")
        return success

    def insert_items_from_q(self, table):
        table = sql_statements[table]
        cur = self.conn.cursor()
        self.execute_query(table["DROP"])
        self.execute_query(table["CREATE"])
        received = 0
        inserted = 0
        q_list = []
        print(self.q_in.qsize())
        while True:
            if self.q_in.empty():
                print("SQL Gnome has no data to push, sleeping...")
                time.sleep(3)
            else:
                data_in = self.q_in.get()
                received = self.q_in.qsize() + inserted
                q_list.append(data_in)
                ins_to_stop = False

                if data_in == self.stop_term:
                    q_list.pop()
                    self.stop_n += 1
                    if self.stop_lim == self.stop_n:
                        inserted += self.insert_many(
                            cur, table["INSERT"], q_list
                        )
                        received = self.q_in.qsize() + inserted
                        print(
                            "\nSQL Gnome finished pushing {}/{} entries!".format(
                                inserted, received
                            )
                        )
                        #self.print_table(table)
                        return False
                    else:
                        ins_to_stop = True

                if len(q_list) > self.ins_size | ins_to_stop:
                    # print("SQL Gnome pushing {} items".format(self.ins_size))
                    inserted += self.insert_many(
                        cur, table["INSERT"], q_list[0 : self.ins_size]
                    )
                    printProgressBar(
                        inserted,
                        received,
                        prefix="SQL Gnome pushing {}/{}".format(
                            inserted, received
                        ),
                    )
                    q_list = []
                    ins_to_stop = False

        # self.print_table()

    def insert_many(self, cur, q_string, items):
        try:
            cur.executemany(q_string, items)
            self.conn.commit()
            return len(items)
        except Exception as e:
            # print("Could not insert \n{}".format(items))
            print("\t Error: {}".format(e))
            return 0
