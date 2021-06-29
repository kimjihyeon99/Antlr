pragma solidity 0.4.4;
contract MedStats {
    final address hosipital;
    unit count;
    mapping(address!x =>bool@x) risk;

    constructor(){
        hospital = me;
        count =0;
    }

    function record(address don, bool r){
        require(hospital == me);
        risk[don] = reveal(r,don);
        count = count + (r ? 1:0);
    }

    function check(bool r){
        require(reaveal(r == risk[me],all));
    }
 }