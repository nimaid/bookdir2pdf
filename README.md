# bookdir2pdf
Merges a directory structure of images into a PDF with nested bookmarks.

```
$ bookdir2pdf.py --help
usage: bookdir2pdf.py [-h] -i INPUT_DIR [-o OUTPUT_FILE]
                      [-s ORDER_NUMBER_SEPARATOR] [-n]
                      [-p [PURIFY [PURIFY ...]]] [-d DPI] [-t TITLE]
                      [-a AUTHOR]
                      [-f [TABLE_OF_CONTENTS_FORMAT [TABLE_OF_CONTENTS_FORMAT ...]]]

Merge nested image directory into PDF with nested bookmarks.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_DIR, --input_dir INPUT_DIR
                        path to nested image directory to merge
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        output file path ( defaults to [input_dir].pdf )
  -s ORDER_NUMBER_SEPARATOR, --order_number_separator ORDER_NUMBER_SEPARATOR
                        the character used to separate the directory ordering
                        numbers from the bookmark names ( like '.' or ')' )
  -n, --no_pdf          just scan directory and print table of contents
  -p [PURIFY [PURIFY ...]], --purify [PURIFY [PURIFY ...]]
                        purify scanned B&W page ( greyscale, sharpen,
                        threshold ), named sub-arguments: (sharpen|s)
                        (threshold|t)
  -d DPI, --dpi DPI     dots-per-inch of the input images
  -t TITLE, --title TITLE
                        the PDF title ( defaults to the directory basename )
  -a AUTHOR, --author AUTHOR
                        the PDF author
  -f [TABLE_OF_CONTENTS_FORMAT [TABLE_OF_CONTENTS_FORMAT ...]], --table_of_contents_format [TABLE_OF_CONTENTS_FORMAT [TABLE_OF_CONTENTS_FORMAT ...]]
                        formatting options for the table of contents, named
                        sub-arguments: (break_limit|b) (number_prefix|p)
                        (number_postfix|a) (indent|i)
```

The PDF here was made using:

`bookdir2pdf.py --input_dir test_dir/ --order_number_separator . --purify sharpen=1`

The `.` is what seperates the ordering numbers from the bookmark name in the directory name. For example, the directory name `01. The First Part` has a `.` between the ordering number `01` and the bookmark name `The First Part`.

The `sharpen=1` means not to sharpen during the purification step.

The bookmark structure can be previewed without actually processing any files:

```
$ bookdir2pdf.py --input_dir test_dir/ --order_number_separator . --no_pdf --table_of_contents_format break_limit=50

... [output removed] ...

                        Example PDF
          by https://github.com/nimaid/bookdir2pdf
                     Table of Contents
-----------------------------------------------------------
Page #1   Cover Page
Page #2   --- Empty Directory Example
Page #2   --- --- Nested Empty Directory Level 1
Page #2   --- --- --- Nested Empty Directory Level 2
Page #2   --- --- --- --- Nested Empty Directory Level 3
Page #3   Empty Directory .name File Example (allows for
          forbidden characters like <>?\/*: and also means
          you can make a really long name like this without
          hitting the path length limit of your OS)
Page #3   The First Part
Page #3   --- Chapter 1
Page #5   --- Chapter 2
Page #7   The Middle Part
Page #7   --- Chapter 3
Page #9   --- Chapter 4
Page #11  The Final Part
Page #11  --- Chapter 5
Page #13  --- Chapter 6
        Page count: 14

... [output removed] ...
```

## Complex Examples
Here are the two complex bookmark structures that prompted me to create this program:

```
                  Electronotes - Builder's Guide & Preferred Circuits Collection
                                        by Bernie Hutchins
                                        Table of Contents
--------------------------------------------------------------------------------------------------
Page #1    Cover Page
Page #5    Table of Contents
Page #7    Part One: Introduction, Basics, Plans
Page #9    --- 1-1. Introduction
Page #11   --- 1-2. Plan Of Attack
Page #12   --- 1-3. The Actual Plan Of The Electronic Music System
Page #13   --- 1-4. Deciding What Will Be In Your System
Page #20   --- 1-5. How To Obtain The Parts You Need
Page #23   --- 1-6. Building Your System
Page #26   --- 1-7. System Integration
Page #27   --- 1-8. Standards Used
Page #28   --- 1-9. Substitution Of Op-Amps
Page #31   --- 1-10. Modular Design
Page #41   Part Two: Construction Practices
Page #43   --- 2-1. Introduction
Page #43   --- 2-2. Hints On Setting Up An Electronic Music Working Area
Page #47   --- 2-3. How I Make My P.C. Boards In A Matter Of A Few Hours
Page #50   --- 2-4. Putting Your Circuit Boards Inside Something
Page #53   --- 2-5. Making Rack Panels
Page #59   --- 2-6. Some More Suggestions On Actually Getting Construction Underway
Page #63   --- 2-7. How To Actually Build Something
Page #63   --- --- Part 1: AN-14 - Parts And Supplies
Page #65   --- --- Part 2: AN-15 - Circuit Boards
Page #67   --- --- Part 3: AN-16 - Soldering In Parts
Page #69   --- --- Part 4: AN-17 - Packaging
Page #71   --- --- Part 5: AN-18 - Miscellaneous Hints
Page #73   Part Three: Preferred Circuits Collection
Page #75   --- Power Supplies
Page #77   --- --- PS-1: AN-1 - Five-Volt One-Amp Power Supplies For TTL
Page #79   --- --- PS-2: AN-2 - Bipolar 15 Volt Supplies For Op-Amps
Page #81   --- --- PS-3: AN-98 - IC Regulators For Small Bench Supplies
Page #83   --- --- PS-4: AN-136 - An Op-Amp Supply Based On A 12.6V Filament Transformer
Page #85   --- --- PS-5-Acc: Crowbar Circuit
Page #85   --- --- PS-Extra: MEH-5j
Page #87   --- Controller Interfaces
Page #88   --- --- CI-1: EN#68 - The ENS-76 Home-Built Synthesizer System - Part 4
Page #98   --- --- CI-2: EN#45 - Controller Interface CI-2
Page #99   --- --- CI-3-Acc: MEH-7b - Ranging And Scaling Unit
Page #100  --- --- CI-4: EN#124 - The ARP Surplus Three-Octave Keyboard
Page #103  --- Voltage-Controlled Oscillators
Page #105  --- --- EN#75 - The ENS-76 Home-Built Synthesizer System - Part 7, VCO Options
Page #109  --- --- --- VCO-1
Page #113  --- --- --- VCO-2
Page #117  --- --- VCO-3: EN#67 - ENS-76 'Utility VCO'
Page #118  --- --- VCO-4: EN#65 - Through-Zero VCO (Hall)
Page #119  --- --- VCO-5: EN#69 - AM-FM Utility VCO Using XR2206 VCO Chip
Page #120  --- --- VCO-6: EN#87 - 2030 VCO
Page #121  --- --- VCO-7: EN#129 - A Voltage-Controlled Oscillator With Through-Zero FM Capability
Page #131  --- Manually-Controlled Oscillators
Page #133  --- --- MCO-1: AN-29 - Simple Sine Wave Oscillators
Page #135  --- --- MCO-2: AN-67 - Simple Triangle-Square Oscillator
Page #137  --- --- MCO-3: AN-79 - Some Simple Sawtooth Wave Generators
Page #139  --- --- MCO-4: EN#88 - Peter Lutz's LFO
Page #140  --- --- MCO-5: EN#53 - Inexpensive Function Generator (Craig Anderton)
Page #141  --- --- MCO-6: EN#44 - Low-Frequency Control Oscillator
Page #141  --- --- MCO-7: EN#83 - Simple Manually Tuned Triangle-Square Generator
Page #143  --- Voltage-Controlled Amplifiers
Page #145  --- --- VCA-1: EN#29(MEH-5c) - VCA Design Example #1 - VCA With Linear Response
Page #146  --- --- VCA-2: EN#34(MEH-5c) - VCA Design Example #2 (Linear And Exponential Controls)
Page #147  --- --- VCA-3: EN#63 - ENS-76 VCA Option 1
Page #147  --- --- VCA-4: EN#87 - Synthesizer Voltage-Controlled Amplifier Using 2020
Page #149  --- Envelope Followers
Page #151  --- --- EF-1: EN#60 - Nicholas Collins' Envelope Follower
Page #152  --- --- EF-2: EN#86 - R. Iodice's Envelope Follower
Page #153  --- --- EF-3: EN#88 - Denny Genovese's Envelope Follower
Page #154  --- --- EF-4: EN#89 - Envelope Follower With Ripple Reduction
Page #155  --- Voltage-Controlled Filters
Page #156  --- --- EN#71 - The ENS-76 Home-Built Synthesizer System - Part 5
Page #158  --- --- --- VCF-1
Page #162  --- --- --- VCF-2
Page #164  --- --- VCF-3: EN#41 - Voltage-Controlled 4-Pole Network
Page #165  --- --- VCF-4: EN#87 - Electronic Music Voltage-Controlled Lowpass Filter
Page #166  --- --- VCF-5: EN#72 - ENS-76 VCF Option 3, Variable-Slope Filter
Page #168  --- --- VCF-6: EN#90 - The High-Ripple VCF
Page #169  --- --- VCF-7: EN#92 - Quasi-Digital Bi-N-Tic Filter (Jan Hall)
Page #170  --- --- VCF-8: EN#97 - Dual SSM-2040 Filter
Page #171  --- Timbre Modulators
Page #173  --- --- TM-1: EN#72 - Timbre Modulator - Option 1
Page #175  --- --- TM-2: EN#84 - An Odd-Harmonic To Even-Harmonic Timbre Modulator
Page #179  --- --- TM-3: EN#72 - Double-Pulse Waveform Shaper (Ian Fritz)
Page #181  --- Envelope Generators
Page #183  --- --- EN#66 - The ENS-76 Home-Built Synthesizer System - Part 2
Page #184  --- --- --- EG-1
Page #187  --- --- --- EG-2
Page #190  --- --- EG-3: MEH-5e - Simple AD Envelope Generator
Page #190  --- --- EG-4: EN#45 - ADSR Envelope Generator #1
Page #191  --- --- EG-5: EN#87 - 2050 External Connections
Page #192  --- --- EG-6: EN#86 - Envelope-Transient Generator
Page #193  --- --- EG-7: EN#92 - AD + AR Envelope Generator (Ian Fritz)
Page #195  --- Balanced Modulators
Page #196  --- --- BM-1: EN#63 - ENS-76 Balanced Modulator - Option 1
Page #197  --- --- BM-2: MEH-5f - Balanced Modulator Design Example
Page #199  --- --- BM-3: EN#134 - Integrated Musical Electronics - Part 2: Balanced Modulator
Page #201  --- --- BM-4: EN#113 - Switchable VCA/Balanced Modulator Circuit Based On The LM/XR
                   13600 Transconductance Amplifier (Ian Fritz)
Page #207  --- Frequency Shifter
Page #209  --- --- EN#83 - The ENS-76 Home-Built Synthesizer System - Part 9, Frequency Shifter
Page #225  --- Sample And Hold Units
Page #227  --- --- S&H-1: MEH-5g - Sample-And-Hold Design Example
Page #228  --- --- S&H-2: EN#61 - Sample And Hold (With Additional Features)
Page #229  --- Slewing Circuits
Page #231  --- --- EN#42 - Slew Limiting Ideas (Paul Titchener, Terry Mikulic)
Page #231  --- --- --- SC-1
Page #231  --- --- --- SC-2
Page #231  --- --- --- SC-3
Page #232  --- --- SC-4: EN#59 - Paul Titchener's Voltage-Controlled Slew Limiter
Page #233  --- Noise Sources
Page #235  --- --- EN#76 - The ENS-76 Home-Built Synthesizer System - Part 8, Random Sources
Page #235  --- --- --- NS-1: ENS-76 Random Source - Option 1
Page #237  --- --- --- NS-2: ENS-76 Random Source - Option 2
Page #242  --- --- --- Further Options
Page #249  --- --- NS-3: EN#30 - ENS-73 Noise Source (Dave Rossum)
Page #249  --- --- NS-4: EN#64 - White Noise Generator
Page #251  --- --- NS-5: AN-143 - Simple Noise Sources
Page #253  --- Analog Delay Lines
Page #255  --- --- ADL-1: EN#72 - Delay Module/Sub-Module Option 1
Page #256  --- --- ADL-2: EN#87 - Delay Line Setup Using MN3005 (Jan Hall)
Page #257  --- --- ADL-3: AN-35 - Delay Line Setup Using The SAD-1024
Page #259  --- Animators
Page #261  --- --- ANM-1: EN#87 - Full Circuit of Multi-Phase Waveform Animator
Page #262  --- --- ANM-2: EN#102 - VC LFO's and Summers
Page #265  Part Four: Appendices
Page #267  --- A. EN#91 - But What Should I Start Building Right Now?
Page #271  --- B. Aids On Obtaining Parts
Page #275  --- C. Troubleshooting
Page #275  --- --- 1 - AN-131
Page #277  --- --- 2 - AN-132
Page #279  --- --- 3 - AN-133
Page #281  --- --- 4 - AN-134
Page #283  --- D. Information On Special Purpose Electronic Music IC's
Page #291  --- E. Useful References
        Page count: 292
```

```
                                    Musical Engineer's Handbook
                                         by Bernie Hutchins
                                         Table of Contents
---------------------------------------------------------------------------------------------------
Page #1    Cover Page
Page #4    Dedication/Acknowledgment
Page #5    Table of Contents
Page #6    Introduction
Page #9    Section 1, Basics
Page #9    --- Chapter 1A: Electronic Music Systems and Their Characterization
Page #9    --- --- Introduction
Page #10   --- --- Example Electronic Music Systems
Page #10   --- --- --- Musique Concrète
Page #10   --- --- --- Voltage-Controlled Systems
Page #11   --- --- --- Computer Point-by-Point Synthesis
Page #12   --- --- --- Computer Control of Analog Synthesizers
Page #12   --- --- --- A Tape Delay Feedback System
Page #13   --- --- The Characterization of the Elements of Electronic Music Systems
Page #15   --- Chapter 1B: Waveforms, Envelopes, Modules, and Control
Page #15   --- --- Introduction
Page #16   --- --- Waveforms
Page #18   --- --- Envelopes
Page #19   --- --- Modules
Page #21   --- --- Control
Page #23   --- Chapter 1C: Basic Mathematics of Musical Engineering
Page #23   --- --- Introduction
Page #24   --- --- Graphs, Linear and Non-Linear Relationships
Page #27   --- --- Multiplication in Graph Quadrants
Page #28   --- --- Scaling of Exponentials and Placement of Exponential Converters
Page #29   --- --- Logarithmic Relationships
Page #31   --- Chapter 1D: Integral Methods of Electrical Engineering
Page #31   --- --- Introduction
Page #32   --- --- Eyeballing The Fourier Series
Page #33   --- --- Mathematics of the Fourier Series
Page #34   --- --- Analysis of Non-Periodic Waveforms - Fourier Transforms
Page #37   --- --- Laplace Analysis
Page #40   --- --- Convolution: Time and Frequency
Page #40   --- --- Autocorrelation - A Convolution
Page #41   --- --- Impulse Response
Page #43   --- Chapter 1E: Topics from Musical Acoustics
Page #43   --- --- Introduction
Page #44   --- --- The Accuracy of Traditional Music
Page #45   --- --- Musical Scales
Page #48   --- --- Block Analysis of Traditional Music
Page #50   --- --- Hearing
Page #51   --- Chapter 1F: Basic Principles of Musical Engineering
Page #51   --- --- Introduction
Page #52   --- --- Basic Goals and Procedures
Page #53   --- --- System Design Philosophy
Page #55   --- --- Communications Between Musicians and Engineers
Page #57   Section 2, Basic Sound Synthesis And Electronic Music Techniques
Page #57   --- Chapter 2A: Subtractive Synthesis
Page #57   --- --- Introduction
Page #58   --- --- Harmonic Content of Waveforms
Page #59   --- --- Amplitude and Harmonic Content Alteration
Page #60   --- --- A Basic Subtractive Synthesis Patch
Page #61   --- --- Subtractive Synthesis Using a Noise Source
Page #61   --- --- Filter Ringing
Page #63   --- Chapter 2B: Additive Synthesis
Page #63   --- --- Introduction
Page #63   --- --- Comparison of Additive and Subtractive Synthesis
Page #64   --- --- The Role of Phase in Additive Synthesis
Page #65   --- --- Addition of Non-Harmonics
Page #66   --- --- Construction of Source Banks
Page #67   --- Chapter 2C: Generalized Modulations
Page #67   --- --- Introduction
Page #69   --- --- Addition of Waveforms
Page #72   --- --- Multiplication of Waveforms
Page #74   --- --- Amplitude Modulation
Page #75   --- --- Frequency Modulation
Page #86   --- --- Formant Modulation
Page #86   --- --- Pulse Modulation
Page #88   --- --- Time Sampling
Page #93   --- Chapter 2D: Control of Musical Structure
Page #93   --- --- Introduction
Page #94   --- --- Control: Electronic, Physical, and Programmable
Page #96   --- --- Control by Tape Recorder
Page #97   --- --- Control in Real Time
Page #98   --- --- Release of Control
Page #99   --- Chapter 2E: Miscellaneous Electronic Music Techniques
Page #99   --- --- Introduction
Page #99   --- --- Tape Manipulations
Page #100  --- --- Tape Techniques Using Delay
Page #101  --- --- Phasing Techniques
Page #102  --- --- Reverberation Units
Page #102  --- --- Ensemble Effects
Page #102  --- --- Resonant Synthesis
Page #104  --- --- Phase Locking
Page #105  Section 3, Electrical Components And Electronic Music Applications
Page #105  --- Chapter 3A: Basic Applications of: Operational Amplifiers
Page #105  --- --- Introduction
Page #106  --- --- First Ideal Characteristic - Infinite Gain
Page #107  --- --- Second Ideal Characteristic - No Input Bias Currents
Page #108  --- --- Third Ideal Characteristic - No Differential Input Voltage When Negative
                   Feedback Is Working
Page #110  --- --- --- The Non-Inverting Amplifier
Page #111  --- --- --- The Inverting Amplifier And Related Structures
Page #114  --- --- --- An Alternative Analysis Of The Inverting Amplifier
Page #116  --- --- --- The Op-Amp Differential Amplifier
Page #116  --- --- --- The Generalized Analog Summer
Page #118  --- --- Working With Real Op-Amps
Page #119  --- --- Compensation and Slew Rate
Page #122  --- --- Input Bias Current
Page #123  --- Chapter 3B: Basic Applications of: Operational Transconductance Amplifiers
Page #123  --- --- Introduction
Page #124  --- --- Basic Setup of the CA3080
Page #124  --- --- Typical Gain Controlled Circuit
Page #125  --- --- Signal Switching Methods
Page #126  --- --- Current Switching Methods
Page #127  --- Chapter 3C: Basic Applications of: Current Differencing Amplifiers
Page #127  --- --- Introduction
Page #128  --- --- Open Loop And Logic Circuits
Page #128  --- --- Positive Feedback
Page #129  --- --- Negative Feedback
Page #131  --- Chapter 3D: Basic Applications of: Analog Multipliers
Page #131  --- --- Introduction
Page #132  --- --- Basic 595 Circuits
Page #132  --- --- Application Hints for Type 595
Page #133  --- --- Two-Quadrant Multipliers
Page #135  --- Chapter 3E: Basic Applications of: IC Timers
Page #135  --- --- Introduction
Page #135  --- --- Monostable (One Shot) Circuits
Page #137  --- --- Astable (Oscillator) Circuits
Page #138  --- --- Special Applications
Page #139  --- Chapter 3F: Basic Applications of: Digital Integrated Circuits
Page #139  --- --- Introduction
Page #139  --- --- Application of Logic Gates
Page #142  --- --- Application of Flip-Flops
Page #144  --- --- Special Applications of MSI Devices
Page #146  --- --- Designing with TTL Logic IC's
Page #147  --- Chapter 3G: Basic Applications of: CMOS Integrated Circuits
Page #147  --- --- Introduction
Page #147  --- --- Basic CMOS Application Considerations
Page #148  --- --- Linear CMOS Applications
Page #149  --- --- The Analog Switch
Page #150  --- --- CMOS Handling Precautions
Page #150  --- --- CMOS Interfacing
Page #151  --- Chapter 3H: Miscellaneous Musical IC's
Page #151  --- --- Introduction
Page #151  --- --- VCO and Function Generator Chips
Page #152  --- --- Top Octave Generators
Page #153  --- --- Binary Dividers
Page #154  --- --- Phase-Locked Loops
Page #155  Section 4, Basic Circuit Designs
Page #155  --- Chapter 4A: Circuits Using IC Amplifiers
Page #155  --- --- Introduction
Page #155  --- --- Audio Circuits
Page #156  --- --- Integrators and Differentiators
Page #156  --- --- Simple Signal Generators
Page #157  --- --- Full-Wave Rectifiers
Page #158  --- --- Peak Detectors
Page #159  --- Chapter 4B: Analysis and Design of Active Filters
Page #159  --- --- Introduction
Page #159  --- --- Terminology of Active Filtering
Page #162  --- --- Example Filter Analysis
Page #163  --- --- --- Low-Pass Butterworth
Page #165  --- --- --- State Variable
Page #166  --- --- --- Chebyshev
Page #167  --- --- --- Other Configurations
Page #169  --- Chapter 4C: Circuits Using Discrete Semiconductors
Page #169  --- --- Introduction
Page #169  --- --- The Basic Bipolar Junction Transistor
Page #170  --- --- Electronic Music Applications for FET's
Page #170  --- --- Circuits Using Transistors for Their Logarithmic Properties
Page #171  --- --- Current Sources
Page #172  --- --- Schmitt Triggers with Transistors
Page #172  --- --- Op-Amp Power Output Stage
Page #173  Section 5, Design Of Conventional Music Modules
Page #173  --- Chapter 5A: Modular Design - General Considerations, Inputs and Outputs
Page #173  --- --- Introduction
Page #175  --- --- Voltage Input Structures
Page #179  --- --- Timing Signal Input Structures
Page #180  --- --- Output Structures
Page #183  --- Chapter 5B: Voltage-Controlled Oscillator Design
Page #183  --- --- Introductory Notes
Page #184  --- --- Introduction
Page #186  --- --- Design of the Basic Oscillator
Page #190  --- --- Design of Exponential Current Stages
Page #198  --- --- Design of Waveshaping Circuits
Page #205  --- --- Design Example
Page #209  --- Chapter 5C: Voltage-Controlled Amplifier Design
Page #209  --- --- Introduction
Page #210  --- --- Design of Two-Quadrant Multipliers
Page #215  --- --- Controlled Current Sources for VCA's
Page #217  --- --- Design Examples
Page #217  --- --- --- VCA Design Example #1
Page #218  --- --- --- VCA Design Example #2 (Linear And Exponential Controls)
Page #219  --- Chapter 5D: Voltage-Controlled Filter Design
Page #219  --- --- Introduction
Page #220  --- --- Control Elements for VCF's
Page #223  --- --- Adapting Current Sources for VCF's
Page #225  --- --- Design Examples
Page #225  --- --- --- #1; Reprint: "A Four Pole Voltage-Controlled Network; Analysis, Design, and
                       Application as a Low-Pass VCF and a Quadrature Oscillator" (from EN#41)
Page #232  --- --- --- #2; Voltage-Controlled State Variable Filter (from EN#37)
Page #233  --- Chapter 5E: Envelope Generator Design
Page #233  --- --- Introduction
Page #234  --- --- Attack-Release (AR) Envelope Generators
Page #235  --- --- Attack-Decay (AD) Envelope Generators
Page #236  --- --- Attack-Decay-Sustain-Release (ADSR) Envelope Generators
Page #239  --- --- Design Example - ADSR
Page #240  --- --- Envelope Delay Units
Page #241  --- --- Design Example - Delay Unit
Page #242  --- --- Special Features
Page #243  --- Chapter 5F: Balanced "Ring" Modulator Design
Page #243  --- --- Introduction
Page #244  --- --- Adapting the Analog Multiplier
Page #245  --- --- Design Example
Page #247  --- Chapter 5G: Sample-and-Hold Design
Page #247  --- --- Introduction
Page #248  --- --- Design Example
Page #249  --- --- Additional Features
Page #251  --- Chapter 5H: Noise and Random Source Design
Page #251  --- --- Introduction
Page #251  --- --- Sources Using Semiconductor Junctions
Page #252  --- --- Design Example
Page #252  --- --- Pseudo-Random Sequencers
Page #255  --- Chapter 5I: Mixer and Multiple Design
Page #255  --- --- Introduction
Page #255  --- --- Design and Placement of Multiples
Page #256  --- --- Design of Mixers
Page #259  --- Chapter 5J: Power Supply Design
Page #259  --- --- Introduction
Page #260  --- --- Determining Power Requirements
Page #260  --- --- The Basic Unregulated Supply
Page #263  --- --- Basic Considerations for Regulators
Page #265  --- --- Integrated Circuit Regulators
Page #265  --- --- --- 5 Volt Supplies
Page #265  --- --- --- ±15 Volt, Low Current Supplies
Page #266  --- --- --- ±15 Volt, High Current Supplies
Page #267  --- --- Protective Circuitry
Page #269  Section 6, New Types Of Modules
Page #269  --- Chapter 6A: Frequency Shifter Design
Page #269  --- --- Introduction
Page #270  --- --- Methods of Frequency Shifting
Page #270  --- --- --- The Double Heterodyning Method
Page #271  --- --- --- The Phase Shift Method
Page #271  --- --- --- Methods of Providing the Quadrature Signal
Page #274  --- --- Reprint of "Design of 90° Phase Difference Networks and application to Frequency
                   Shifter Design" (EN#43)
Page #282  --- --- Calculation of Poles of 90° Phase Difference Networks by Weaver's Method
Page #283  --- --- Determining the Required Accuracy
Page #287  --- Chapter 6B: Pitch and Envelope Followers
Page #287  --- --- Introduction
Page #287  --- --- Pitched Signal Production
Page #288  --- --- Pitch Extraction Based on Spectral Information or Pattern Recognition
Page #289  --- --- An Experimental Pitch Extractor and Envelope Follower
Page #291  --- Chapter 6C: Modules Employing Analog Delay Lines
Page #291  --- --- Introduction
Page #292  --- --- Applications Using Mixtures of Delayed and Original Signals
Page #292  --- --- Phasing
Page #293  --- --- Recursive Structures
Page #293  --- --- Reverberation Devices
Page #295  --- Chapter 6D: Transform Devices
Page #295  --- --- Introduction
Page #295  --- --- Comparison of Transform Approaches and the Traditional Approaches
Page #296  --- --- A Hadamard Transform Device
Page #299  Section 7, Controllers And Interface Units
Page #299  --- Chapter 7A: Design of Controllers
Page #299  --- --- Introduction
Page #299  --- --- Keyboards (Discrete Controllers)
Page #300  --- --- Continuous Controllers
Page #302  --- --- Miscellaneous Controllers
Page #303  --- Chapter 7B: Design of Controller Interfaces
Page #303  --- --- Introduction
Page #304  --- --- Keyboard Interfaces
Page #308  --- --- Use of Keyboard Interfaces with Other Units
Page #309  --- --- Digital Interfaces
Page #309  --- --- Digital Counting Interfaces
Page #310  --- --- Touch Control
Page #311  --- --- Touch Sensitivity Translators
Page #312  --- --- Polyphonic Controls and Systems
Page #313  --- Chapter 7C: Design of Sequencers
Page #313  --- --- Introduction
Page #313  --- --- The Characterization of Sequencers
Page #314  --- --- Bucket Brigade Sequencers
Page #316  --- --- The Sample-and-Hold as a Sequencer
Page #316  --- --- Digital Sequencers
Page #317  Section 8, Musical Engineering Operations
Page #317  --- Chapter 8A: Overall Design Considerations
Page #317  --- --- Introduction
Page #318  --- --- Design Steps
Page #318  --- --- Selecting the Number of Modules
Page #319  --- --- Breaking Design Deadlocks
Page #320  --- --- Documentation
Page #321  --- Chapter 8B: Construction
Page #321  --- --- Introduction
Page #321  --- --- Preparation of Circuit Boards
Page #323  --- --- Soldering and Soldering Irons
Page #323  --- --- Wiring of Circuit Boards
Page #325  --- --- Panel Preparation and Wiring
Page #325  --- --- Living With Patch Cords
Page #327  --- Chapter 8C: Troubleshooting
Page #327  --- --- Introduction
Page #328  --- --- Checking the Obvious
Page #328  --- --- Learning What Should be Happening
Page #328  --- --- Isolating the Trouble
Page #329  --- --- Some Troubleshooting Rules
Page #329  --- --- Checking Certain Modules
Page #330  --- --- Troubleshooting Designs and Patches
Page #330  --- --- Special Problems and Techniques
Page #331  Section 9, References
Page #331  --- Chapter 9A: Math Tables
Page #331  --- --- Introduction
Page #331  --- --- Constants
Page #332  --- --- Conversion Factors
Page #332  --- --- Fractional Roots of Two
Page #332  --- --- Rules for Logs and Exponentials
Page #333  --- --- Trig. Identities
Page #333  --- --- Relations between Exponentials and Trig. Functions
Page #333  --- --- Relationships with Bessel Functions
Page #334  --- --- Tables of Trig. Functions
Page #334  --- --- Tables of Bessel Functions (Jₙ and Iₙ)
Page #335  --- --- --- Bessel Functions Of The First Kind Jₙ(x)
Page #336  --- --- --- Modified Bessel Functions Iₙ(x)
Page #339  --- Chapter 9B: Engineering References
Page #339  --- --- Resistor Color Code
Page #339  --- --- Butterworth Polynomials
Page #340  --- --- Table of 5% Resistor Ratios
Page #341  --- --- Laplace Transform Pairs
Page #343  --- Chapter 9C: Electrical Component Data
Page #343  --- --- Introduction
Page #344  --- --- Linear IC's
Page #345  --- --- Arrays
Page #346  --- --- Digital IC's
Page #351  --- Chapter 9D: Reprint Papers
Page #351  --- --- Introduction
Page #353  --- --- "Experimental Electronic Music Devices Employing Walsh Functions" by Bernard A.
                   Hutchins, Jr. - Reprinted from J. Aud. Eng. Soc. 12 #8, Oct. 1973, pg. 640-645
                   with the permission of the author
Page #359  --- --- "Some Notes on the Generation of Sine Waves by Walsh Functions"
Page #371  --- Chapter 9E: Bibliography of Handbook Topics
Page #371  --- --- Introduction
Page #371  --- --- Bibliography, Chapters 1a to 8c
Page #375  Index
        Page count: 376
```