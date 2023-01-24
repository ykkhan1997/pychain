import React,{useState,useEffect} from "react";
import { Link } from "react-router-dom";
import Transaction from "./Transaction";
import { API_BASE_URL, SECONDS_JS } from "../config";
import history from "../history";
import { Button } from "react-bootstrap";
const POOL_INTERVAL=10*SECONDS_JS;
export default function TransactionPool() {
    const [transactions,setTransaction]=useState([]);
    const fetchTransaction=()=>{
        fetch(`${API_BASE_URL}/transactions`)
        .then(response=>response.json())
        .then(json=>{
            console.log('transactions json',json);
            setTransaction(json);
        });
    }
    useEffect(()=>{
        fetchTransaction();
        const Interval_id=setInterval(fetchTransaction,POOL_INTERVAL);
        return ()=>clearInterval(Interval_id);
    },[]);
    const fetchMineBlock=()=>{
        fetch(`${API_BASE_URL}/blockchain/mine`)
        .then(response=>response.json())
        .then(json=>{
            alert('Success!');
            history.push('/blockchain');
        })
    }
  return (
    <div className="TransactionPool">
        <h3>TransactionPool</h3>
        <Link to='/'>Home</Link>
        <div>
            {
                transactions.map(transaction=>(<div key={transaction.id}>
                    <hr/>
                    <Transaction transaction={transaction}/>
                </div>))
            }
        </div>
        <div>
            <Button variant="danger" onClick={fetchMineBlock}>Mine a Block For These Transaction</Button>
        </div>
    </div> 
  )
}
