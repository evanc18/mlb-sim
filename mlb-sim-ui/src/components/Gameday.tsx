import { useState, useEffect } from "react";
import axios from "axios";
import { List } from "@mui/material";

interface GamedayProps {
    onSim: (game: any) => void;
}

interface GamedayState {
    records: any
}

const Gameday = ({onSim}: GamedayProps) => { 

    const [state, setState] = useState<GamedayState>({
        records: undefined
    })

    useEffect(() => {
        axios.get('https://statsapi.mlb.com/api/v1/standings?leagueId=103')
        .then(response => setState({...state, records: response.data.records}))
        .catch(error => console.error(error));
    })

    //Convert js date format to mlb-api format
    const formatDate = (date: Date) => {
        const day = date.getDate();
        const month = date.getMonth() + 1;
        const year = date.getFullYear();
        return `${year}-${month}-${day}`;
      }

    const gameurl = (gamepk: Number) => "https://statsapi.mlb.com/api/v1.1/game/"+gamepk+"/feed/live";
    const scheduleurl = (startDate: Date, endDate: Date) => "https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate="+startDate+"&endDate="+endDate;

    let annotation = [];
    return (
        <div>
            <List></List>
        </div>
    )
}