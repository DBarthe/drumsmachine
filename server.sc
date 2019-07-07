s.boot
s.plotTree
NetAddr.langPort;
NetAddr.localAddr;

(
SynthDef(\kick, {
	| out = 0, pan = 0, amp = 0.3,
	attack = 0, decay = 0.08, pitchLow = 60, pitchHigh = 440, pitchCurve = -4, release = 0, dist = 0 |
	var snd;
	var pitchEnv, ampEnv;
	var click;

	pitchEnv = EnvGen.ar(Env.adsr(attack, decay, pitchLow / pitchHigh, 0, pitchHigh, pitchCurve),  doneAction: 2);
	ampEnv = EnvGen.ar(Env.linen(attack, decay, release + 0.001, 1, 'lin'), doneAction: 2);

    click = LPF.ar(Formant.ar(910, 4760, 2110), 3140) * EnvGen.ar(Env.perc(0.001, 0.01)) * 0.15;

	snd =  (1+dist) * SinOsc.ar(pitchEnv) * ampEnv  + click;
	snd = snd.tanh;

    Out.ar(out, Pan2.ar(snd, pan, amp));
}).add;

SynthDef(\snare, {
    |out = 0, pan = 0, amp = 0.5|
    var pop, popAmp, popFreq;
    var noise, noiseAmp;
    var snd;

    // pop makes a click coming from very high frequencies
    // slowing down a little and stopping in mid-to-low
	popFreq = EnvGen.ar(Env([3261, 410, 50], [0.005, 0.01], curve: \exp));
    popAmp = EnvGen.ar(Env.perc(0.001, 0.11)) * 0.7;
    pop = SinOsc.ar(popFreq) * popAmp;
    // bandpass-filtered white noise
    noiseAmp = EnvGen.ar(Env.perc(0.001, 0.23), doneAction: 2);
    noise = BPF.ar(WhiteNoise.ar, 810, 1.8) * noiseAmp;

    snd = (pop + noise) * 1.3;

    Out.ar(out, Pan2.ar(snd, pan, amp));
}).add;

SynthDef(\openhat, {
    |out = 0, pan = 0, amp = 0.3|
    var click, clickAmp;
    var noise, noiseAmp;
    var snd;

    // noise -> resonance -> expodec envelope
    noiseAmp = EnvGen.ar(Env.perc(0.001, 0.85, curve: -8), doneAction: 2);
    noise = Mix(BPF.ar(ClipNoise.ar, [4010, 4151], [0.15, 0.56], [1.0, 0.6])) * 0.7 * noiseAmp;

    snd = noise;

    Out.ar(out, Pan2.ar(snd, pan, amp));
}).add;

SynthDef(\closedhat, {
    |out = 0, pan = 0, amp = 0.3|
    var click, clickAmp;
    var noise, noiseAmp;
    var snd;

    // noise -> resonance -> expodec envelope
    noiseAmp = EnvGen.ar(Env.perc(0.001, 0.1, curve: -8), doneAction: 2);
    noise = Mix(BPF.ar(ClipNoise.ar, [4010, 4151], [0.15, 0.56], [1.0, 0.6])) * 0.7 * noiseAmp;

    snd = noise;

    Out.ar(out, Pan2.ar(snd, pan, amp));
}).add;

// adapted from a post by Neil Cosgrove (other three are original)
SynthDef(\clap, {
    |out = 0, amp = 0.5, pan = 0, dur = 1|
    var env1, env2, snd, noise1, noise2;

    // noise 1 - 4 short repeats
    env1 = EnvGen.ar(
        Env.new(
            [0, 1, 0, 0.9, 0, 0.7, 0, 0.5, 0],
            [0.001, 0.009, 0, 0.008, 0, 0.01, 0, 0.03],
            [0, -3, 0, -3, 0, -3, 0, -4]
        )
    );

    noise1 = WhiteNoise.ar(env1);
    noise1 = HPF.ar(noise1, 600);
    noise1 = LPF.ar(noise1, XLine.kr(7200, 4000, 0.03));
    noise1 = BPF.ar(noise1, 1620, 3);

    // noise 2 - 1 longer single
    env2 = EnvGen.ar(Env.new([0, 1, 0], [0.02, 0.18], [0, -4]), doneAction:2);

    noise2 = WhiteNoise.ar(env2);
    noise2 = HPF.ar(noise2, 1000);
    noise2 = LPF.ar(noise2, 7600);
    noise2 = BPF.ar(noise2, 1230, 0.7, 0.7);

    snd = noise1 + noise2;
    snd = snd * 2;
    snd = snd.softclip;

    Out.ar(out, Pan2.ar(snd,pan,amp));
}).add;
)

(
OSCdef.new(
	\kick,
	{
		arg msg, time, addr, port;
		[msg[0]].postln;
		Synth.new(\kick, [\dist, 1, \release, 0.45, \attack, 0.01, \decay, 0.2, \pitchHigh, 300, \pitchLow, 60, \pitchCurve, -5] );

	},
	'/kick'
);

OSCdef.new(
	\snare,
	{
		arg msg, time, addr, port;
		[msg[0]].postln;
		Synth.new(\snare);

	},
	'/snare'
);

OSCdef.new(
	\openhat,
	{
		arg msg, time, addr, port;
		[msg[0]].postln;
		Synth.new(\openhat);

	},
	'/openhat'
);

OSCdef.new(
	\closedhat,
	{
		arg msg, time, addr, port;
		[msg[0]].postln;
		Synth.new(\closedhat);

	},
	'/closedhat'
);

OSCdef.new(
	\clap,
	{
		arg msg, time, addr, port;
		[msg[0]].postln;
		Synth.new(\clap);

	},
	'/clap'
)
);




