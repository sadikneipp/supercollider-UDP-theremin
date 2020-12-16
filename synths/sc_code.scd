~theremin = { arg freq = 440;
   SinOsc.ar(freq, 0, 0.1)
}.play;

(
f = { |msg, time, addr|
    if(msg[0] == '/theremin.freq') {
        "time: %\nmessage: %\n".postf(time, msg);
		~theremin.set(\freq, msg[1]);
    }
};
thisProcess.addOSCRecvFunc(f);
);