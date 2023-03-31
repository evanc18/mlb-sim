import pybaseball as pb


def reverse_lookup_player(player_ids, key_type='mlbam'):
    return pb.playerid_reverse_lookup(player_ids, key_type=key_type)


def lookup_player(last, first, fuzzy=True):
    return pb.playerid_lookup(last, first, fuzzy)
