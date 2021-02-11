import {URCL8, URCL16} from "./vm.ts"

let data = Deno.readFileSync(Deno.args[0]);
let vm;
try {
vm = new URCL8(data[0], data[1], data[2]);
} catch(e) {
    try {
        vm = new URCL16(data[0], data[1], (data[2] << 8) | data[3]);  
        //console.log((data[2] << 8) | data[3])      
    } catch(e) {
        vm = new URCL16(16, 0, 1);
    }
}
vm.load(data[0] <= 8 ? data.slice(3) : data.slice(4));
vm.start();