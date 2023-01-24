import React,{useState,useEffect}from 'react'
import logo from '../assets/logo.png'
import { API_BASE_URL } from '../config';
import { Link } from 'react-router-dom';
export default function App() {
  const [walletInfo,setWalletInfo]=useState({});
  useEffect(()=>{
    fetch(`${API_BASE_URL}/wallet-info`)
    .then(response=>response.json())
    .then(json=>setWalletInfo(json))
  },[])
  const {address,balance}=walletInfo;
  return (
    <div className='App'>
      <img className='logo' src={logo}alt='Alternate-log'/>
      <h3>Welcome to Blockchain</h3>
      <div>Address: {address}</div>
      <div>Balance: {balance}</div>
      <Link to='/blockchain'>Blockchain</Link>
      <Link to='/conduct-transaction'>Conduct Transaction</Link>
      <Link to='/transaction-pool'>Transaction Pool</Link>
    </div>
  )
}
