# 三联吡啶配位驱动自组装：从离散多边形到分形与巨型金属超分子结构

> 自动生成于 2026-04-07 | 基于84篇文献数据库
> 迭代轮次: 6 + 收尾 | 总字数: 约3800字

## 1. 引言

配位驱动自组装（coordination-driven self-assembly）是超分子化学的核心研究范式之一，通过方向性金属配位键自发将有机配体与金属离子组织成具有精确尺寸和形状的离散结构，在纳米科技、药物递送、催化和功能材料等领域具有广泛应用前景。与共价合成相比，配位键的可逆性赋予自组装体系"错误自修复"能力，使复杂结构得以通过单一热力学过程以高产率实现——这是传统有机合成难以比拟的优势。

在众多配体骨架中，2,2':6',2''-三联吡啶（terpyridine，tpy）以其独特的性质脱颖而出。tpy 通过三个吡啶氮原子以三齿方式螯合金属离子，在金属两侧形成线性排列的 tpy-M-tpy 配合物，与仅能提供弯折连接的联吡啶（bipyridine）形成本质区别。这种线性连接方式，结合可通过金属离子种类调控的配位强度（从动力学惰性的 Ru(II) 到热力学可逆的 Zn(II)/Cd(II)），使 tpy 成为构建复杂二维和三维金属超分子的理想平台。

过去二十年间，基于 tpy 的配位驱动自组装经历了从简单多边形到分形架构、再到巨型多组分超分子和介观尺度结构的跨越式发展，伴随着表征方法（尤其是 TWIM-MS 和低温 STM）的革命性进步。本文以 84 篇文献为基础，系统综述 tpy 体系精准自组装策略的发展脉络：从解决"多组分混合物"挑战的三类策略，到分形几何在分子尺度的化学实现（Sierpinski 三角形、六角垫片、多代超分子分形），再到逐步策略驱动的巨型多组分星形超分子与 20 nm 介观尺度的突破，最后讨论金属离子多样性与功能化方向，并展望该领域的未来挑战。

## 2. tpy 配体的配位特点与自组装基础

2,2':6',2''-三联吡啶（terpyridine，简称 tpy）是配位驱动自组装领域最重要的配体骨架之一。三联吡啶通过三个吡啶氮原子螯合金属离子，形成具有线性几何特征的 tpy-M-tpy 八面体配合物，两个 tpy 配体在金属离子两侧呈反式排列。这一独特的线性连接方式使 tpy 成为构建一维和二维金属超分子结构的理想组件，与形成角状连接的联吡啶（bipyridine）体系有本质区别。

tpy 与不同过渡金属离子的配位强度存在显著差异。Ru(II)-tpy 配位具有动力学惰性，在常规条件下近乎不可逆，常被用于预构建稳定的金属有机配体；Fe(II)-tpy 配位亦较强，但在加热或溶剂辅助条件下可实现热力学控制；而 Zn(II) 和 Cd(II) 与 tpy 的配位属于弱可逆结合，构成热力学自组装体系的首选金属离子[1,2]。这种金属依赖性配位强度的梯度为逐步组装策略奠定了基础。

然而，tpy 体系的自组装精确控制存在固有挑战。当使用夹角约为 120° 的二齿 tpy 配体时，由于 tpy-Zn(II)-tpy 连接的 180° 线性特征与 120° 配体夹角的结合，理论上应形成六边形大环。然而，Wang 等人发现[3]，此类体系在热力学控制下往往产生从五聚体到九聚体的宽泛混合物，而非单一结构，严重制约了精准组装的实现。相比之下，夹角为 60° 的二齿 tpy 配体能够稳定地形成三角形金属大环。Hwang 等人早在 2005 年即报道了利用 1,2-双(tpy-4-乙炔基)苯（60° 角）与 Fe(II) 和 Ru(II) 自组装三角形大环，并通过逐步法实现了含不同金属中心的异核三角形 [2Ru(II)Fe(II)] 的选择性制备[4]。

表征手段的进步对这一领域的发展起到了关键推动作用。Chan 等人于 2009 年率先将行波离子迁移质谱（TWIM-MS）应用于 tpy 基超分子表征[5]，利用气相离子迁移率差异区分了具有相同 m/z 的环状和线性异构体：紧凑的环状六镉大环 [Cd₆L₆]¹²⁺ 的漂移时间（5.13 ms）明显短于延展的线性聚合物（6.45 ms），首次为 tpy 自组装体提供了确定性结构证明。此后，ESI-MS 结合 TWIM-MS、2D DOSY NMR 及原子力显微镜（AFM）构成了该领域的标准表征体系，使研究者得以在溶液态和气相中交叉验证组装结构的组成、尺寸和形状。

## 3. 从多组分混合物到离散大环：精准自组装的策略突破

tpy 体系的一个核心挑战在于：当配体夹角接近 120° 时，自组装产物往往是一系列不同核数大环的混合物，难以分离和应用。突破这一瓶颈的关键在于发展了三类互补策略。

**策略一：多组分化学计量控制**。Wang 等人在 2011 年报道了一种多组分辐条轮结构[6]，通过将六齿核心配体 T6、三齿轮辋配体 T3 和 Cd(II) 以精确的 1:6:12 比例混合，利用几何约束（T6 的六重对称性迫使六个 T3 单元围绕其排列）和热力学自修复，以高达 94% 的分离产率获得了具有 D₆ₕ 对称性的离散二维超分子辐条轮（分子量 13,303 Da，TEM 观测直径约 5.6 nm）。TWIM-MS 碰撞截面（CCS）实验值（1609.7 Å²）与理论值（1750.8 Å²）的高度吻合，证实了结构的精准性。

**策略二：预组装限制自由度**。利用 Ru(II)-tpy 配位的高稳定性，研究者预先合成含 Ru(II) 的二聚体金属有机配体，再将其与其他 tpy 配体和弱配位金属离子组合。Chan 等人于 2012 年展示了这一策略[7]：通过引入预组装 Ru(II) 二聚体，消除了单纯使用 Zn(II)/Cd(II) 时形成不需要的三聚体副产物的竞争，定向合成了领结（bowtie）形大环。以 meta-取代配体代替 para-取代配体，则同样以化学计量组装方式获得了蝴蝶（butterfly）形构型异构体。两种异构体在 TWIM-MS 中表现出截然不同的漂移时间，证明不同拓扑形状产生了可辨识的分子尺寸差异。

**策略三：提高配位位点密度（DOCS，Density of Coordination Sites）**。Jiang 等人在 2014 年提出并验证了 DOCS 策略[3]：将二齿（120° 角）tpy 配体升级为三齿和四齿多位 tpy 配体，大幅提升了每个配体单元的配位约束程度，将原本产生五聚体至九聚体混合物的自组装体系，精准地导向单一的六角花环结构 [Zn₉LA₆]（直径约 5.5 nm）和 [Zn₁₂LB₆]（直径约 5.8 nm）。TWIM-MS 证实每个电荷态仅呈单一窄漂移分布，表明产物为高刚性的单一离散组分，与二齿配体组装的高柔性混合物形成了鲜明对比。

上述三类策略从不同角度出发，共同建立了 tpy 精准自组装的方法论框架，为后续构建更复杂的分形和多组分巨型超分子奠定了基础。

## 4. 分形架构的化学实现：Sierpinski 三角形与六角垫片

分形几何由 Mandelbrot 于 1975 年提出，描述了自然界中广泛存在的自相似性结构。将精确的数学分形概念付诸化学合成，是超分子化学的重大挑战。tpy 体系因其方向性明确的线性连接和广泛的金属兼容性，成为实现分形化学的首选平台。

**分子 Sierpinski 六角垫片**。Newkome 等人于 2006 年在《Science》上报道了首个非树枝状分形超分子——Sierpinski 六角垫片[8]。他们通过逐步策略，先将双 Ru(III) 单体与三-tpy 配体在回流条件下反应，以 35% 产率获得关键的异三聚体，再进一步组装成六聚体（产率 31%），最终加入 FeCl₂ 处理，定量得到最终的 Sierpinski 六角垫片。该分形结构包含 36 个 Ru 和 6 个 Fe 离子，纳米级尺寸约 5 nm，在透射电子显微镜（TEM）和原子力显微镜（AFM）下清晰可见六角形环状结构。这一工作的核心策略是利用 tpy-Ru(II)-tpy 动力学惰性作为结构骨架的"锁"，再以 tpy-Fe(II)-tpy 的热力学可逆性完成最终闭合，两种金属离子的功能分工体现了 tpy 体系的独特优势。

**Sierpinski 三角形：一步多组分法**。Sarkar 等人于 2014 年实现了首个基于 tpy-Cd(II)-tpy 连接的第一代 Sierpinski 三角形的一步多组分自组装[9]。他们设计了几何互补的"K"形四齿 tpy 配体（提供分叉节点）和"V"形二齿 tpy 配体（提供边单元），以精确的 1:1:3（"K":"V":Cd²⁺）化学计量比混合，在室温下 30 分钟内以 >95% 的产率得到 D₃ₕ 对称的 Sierpinski 三角形。ESI-TWIM-MS 在所有电荷态下均显示单一窄条带，与理论碰撞截面高度吻合；TEM 直接观察到顶点间距约 5.6 nm 的三角形分子。该"互补配体对"策略的巧妙之处在于：K 形配体无法与自身形成稳定循环，V 形配体也难以单独形成小环，只有二者按特定比例结合，才能导向唯一的 G1 Sierpinski 产物。

**分子拼图策略：向更高代数迈进**。直接混合法在制备 G2 和 G3 Sierpinski 三角形时遭遇了根本性困难：配体自分选倾向于生成低代三角形，导致不同代产物的竞争性混合。Jiang 等人于 2017 年提出"分子拼图（molecular puzzling）"策略[10]：利用 Ru(II)-tpy 动力学惰性，将 G2 三角形所需的整个配体骨架预先合成为含 4 个游离 tpy 的金属有机配体 LA，再与 Zn(II) 以近乎定量的产率（>95%）组装为 G2 三角形（分子量 10,159 Da）；类似地，含 7 个游离 tpy 的配体 LB 与 Cd(II) 组装给出 G3 三角形（流体动力学半径 3.77 nm，与计算值 3.83 nm 高度吻合）。"分子拼图"策略的本质是：通过预构建完整的组装"拼图块"，排除低代产物的竞争通路，实现高代分形的按需精准合成。

## 5. 逐步策略与巨型多组分星形超分子

随着 tpy 超分子化学向更复杂结构迈进，配体组分数量和结构尺寸的双重提升提出了新的合成挑战。仅靠热力学控制的一步组装，往往难以驱动含三种以上不同 tpy 配体的多组分体系走向单一产物。**逐步策略（stepwise strategy）**为此提供了系统性解法：先利用 Ru(II)-tpy 连接的动力学稳定性合成精确的金属有机配体（MOLs），再以 Zn(II) 或 Cd(II) 的热力学可逆配位完成最终自组装，两步的清晰分工使结合三种乃至更多 tpy 配体成为可能。

**超级雪花系列**。Zhang 等人于 2017 年首次报道了由三种 tpy 配体（双齿配体 L1、三齿配体 L2 和六齿核心配体 L3）以及两种金属离子（Ru(II) 和 Zn(II)）构成的菱形星形超分子——超级雪花[11]。超级雪花 S1 含 3 种 tpy 有机配体和 2 种金属离子，分子量 20,830 Da，直径约 9.8 nm；S2 将三苯胺基团引入侧链，分子量扩大至 26,718 Da，直径约 9.4 nm。TWIM-MS 在每个电荷态均显示单一窄带分布，TEM 清晰呈现星形空心结构。此后，Zhang 等人进一步通过改变 Y 形配体的臂长，分别获得了直径约 10.4 nm（S3）和 11.8 nm（S4）的超级雪花[12]，展示了模块化放大的设计逻辑，并揭示了动态配体交换行为与臂长差异的定量关系——臂长差异小时发生完全交换，差异大时体系呈现"自分选"（self-sorting），不同超分子完全不发生组分混合。

**超分子五角星与六角星**。Jiang 等人于 2017 年尝试利用非对称金属有机配体 LA 与 Cd²⁺/Fe²⁺ 自组装六角星，却出乎意料地获得了五角星 [M₁₀LA₅]³⁰⁺ 而非六角星[13]。详细研究表明，配体 LA 中延伸 tpy 的轻微柔性和不同配位键长的微小差异使配体夹角偏离理想六角形的要求，从而驱动体系走向五重对称的五角结构。通过重新设计更对称的配体 LB 并以 Fe²⁺ 在较高温度下组装，最终以高产率分离出纯净的超分子六角星 [Fe₁₂V₃LB₃]³⁶⁺（流体动力学半径 3.77 nm）。这一案例深刻揭示了配体几何设计的精密性：微小的分子柔性可以在五角形和六角形拓扑之间造成截然不同的结果，从而为通过配体设计调控超分子拓扑提供了重要启示。

## 6. 五代超分子分形与金属离子效应

**五代超分子分形（G1–G5）**。在分形化学系统性构建方面，Wang 等人于 2018 年完成了迄今最完整的超分子分形系列，以三苯胺（triphenylamine）基序作为几何控制核心，通过 Sonogashira 偶联和/或 tpy-Ru(II)-tpy 连接制备了一系列复杂 Ru(II)-有机构建块（ROBBs），再与 Zn(II) 精确配位组装了从 G1 到 G5 共五代超分子分形[14]。G1 基本单元分子量仅 2,722 Da；G5（[Zn₁₂LE₂]）含 12 个重复单元，是最大的离散分形之一。关键在于，所有五代分形均以高产率获得（G3 产率高达 94%），并通过 ESI-MS、TWIM-MS、TEM 全面表征。两个最大的分形（G4/G5）进一步展示了层级自组装功能：它们能在固/液界面或溶液中自发组装成有序的超分子纳米结构，赋予了分形在材料科学中的潜在应用价值。吸收光谱中 285、325 nm 处的 π→π* 带和 485 nm 处 Ru(II)-tpy 金属到配体电荷转移（MLCT）跃迁以及 390 nm 处三苯胺到 tpy 分子内电荷转移带，为各代分形的结构指认提供了光谱指纹。

**金属离子效应**。长期以来，直接组装大型离散 tpy 超分子的可用金属离子主要限于 Cd(II)、Zn(II) 和 Fe(II) 三种。Wang 等人于 2020 年系统拓展了这一范围，首次将 Mn(II)、Co(II)、Ni(II) 和 Cu(II) 引入大型离散 tpy 超分子自组装[1]，在同一三苯胺骨架配体体系下以七种二价过渡金属分别自组装了 M₁₂L₆ 六聚体分形结构，实验分子量从 SA-Mn 的 14,766 Da 到 SA-Cd 的 15,455 Da。Fe(II) 体系的自组装需要采用 CF₃CH₂OH 作为共溶剂来削弱 tpy-Fe 配位强度、增加可逆性，体现了不同金属离子对反应条件的差异要求。通过碰撞诱导解离质谱（CID-MS）系统研究了七种金属超分子在气相中的结构稳定性顺序，同时通过质谱实时监测溶液中的动态配体交换过程动力学，揭示了不同金属离子配位惰性的排序规律。值得注意的是，Cr(II)、Hg(II)、Ir(III)、Ru(II)、碱土金属及镧系元素均不能形成类似的离散结构，表明可用于 tpy 大型离散组装的金属离子集合仍有明确边界，为未来功能性金属超分子设计提供了选择依据。

## 7. 介观尺度探索、层级自组装与功能化

**Kandinsky 圆：嵌套同心超分子**。自然界中广泛存在的同心嵌套结构（如洋葱层、树的年轮）在超分子水平上的化学模拟长期以来是重大挑战。Wang 等人于 2018 年设计并组装了三代"Kandinsky 圆"——离散的嵌套同心六角形超分子[15]。其核心是利用吡喃鎓盐化学模块化合成多齿 tpy 配体系列（双齿至八齿），再与 Cd(II) 自组装：G2（双层嵌套）分子量 17,964 Da，直径约 7.9 nm；G3（三层）达 27,713 Da，直径 9.8 nm；G4（四层）38,352 Da，直径约 11.4 nm。碰撞诱导解离实验表明稳定性随嵌套层数增加而提升。重要的是，这些嵌套超分子能通过层级自组装形成管状纳米结构，并对革兰氏阳性病原体耐甲氧西林金黄色葡萄球菌（MRSA）显示出显著的抗菌活性（MIC ~2 μg/mL），而相应的游离配体几乎无活性，表明超分子结构本身是抗菌功能的关键，很可能通过跨膜通道机制发挥作用。

**向介观尺度推进：20 nm 离散六角网格**。大多数离散配位驱动自组装结构的尺寸小于 10 nm，而 10–100 nm 介观尺度的离散结构极为罕见。Zhang 等人于 2020 年在《Nature Chemistry》上报道了一种突破性的分级自组装策略[16]：仿照蛋白质折叠过程，将含 Ru(II) 预组装连接的多 tpy 配体单元首先在 Fe²⁺ 作用下完成分子内折叠（内向自组装），形成中间六角体，再以额外 Fe²⁺ 驱动分子间自组装，最终获得直径约 20 nm、分子量约 65,790 Da 的二维离散六角网格。ESI-MS 检测到 29+ 至 66+ 的系列电荷态，TWIM-MS 给出单组漂移信号，DOSY 扩散系数（7.08 × 10⁻¹¹ m²/s）均与单一离散物种一致。此外，低温超高真空扫描隧道显微镜（STM）以亚分子分辨率直接成像了该六角网格及其八种异构体，是迄今 tpy 超分子体系中最为精确的结构成像。这一工作将 tpy 配位驱动自组装的结构尺度推进到 20 nm 量级，有效填补了分子尺度（<10 nm）与纳米材料尺度（>100 nm）之间的空白。

**动力学与热力学控制的机制揭示**。2020 年，Wang 等人利用类似的逐步策略构建了含三种金属离子（Ru/Fe 或 Co）的巨型超分子，并通过测量 162 个 STM 成像结构统计分析了 8 种位置异构体的出现概率[17]。结合密度泛函理论（DFT）计算，实验概率与理论概率的比对揭示：尽管动力学控制在某些步骤中发挥作用，体系总体上受热力学控制，热力学更稳定的异构体在实验中出现频率更高。这一发现为深入理解 tpy 超分子自组装机制提供了实验基础，也为通过条件调控（温度、溶剂、浓度）实现对特定异构体的选择性合成指明了方向。

## 8. 总结与展望

本文系统综述了以 tpy 为核心配体的配位驱动自组装研究进展。tpy-M-tpy 线性连接结合金属依赖性配位强度梯度，催生了三大精准自组装策略：多组分化学计量控制、预组装限制自由度（Ru(II) 金属有机配体）以及提高配位位点密度（多齿 tpy 配体）。基于这些策略，研究者实现了数学分形（Sierpinski 三角形、六角垫片）在分子尺度的精确化学表达，构建了从 G1 到 G5 的超分子分形系列，并通过逐步策略组装了包含三种以上 tpy 配体的巨型多组分星形超分子（超级雪花系列，直径 8.5–11.8 nm）。金属离子范围被从最初的 3 种拓展至 7 种，为功能性金属超分子的设计提供了更大选择空间。2020 年，分级自组装策略成功将离散 tpy 超分子的尺寸推进至 20 nm 介观尺度，并在 Kandinsky 圆和六方棱柱等结构中展示出抗菌等生物活性功能。

然而，该领域仍面临若干挑战：（1）**尺度突破**：如何进一步推进至 50–100 nm 介观尺度而维持离散性和单一性；（2）**功能导向设计**：将超分子结构的几何与空腔特性与催化、传感、药物递送等功能精确关联；（3）**动态响应性**：利用 tpy 配位的可逆性设计对光、pH、氧化还原等外部刺激响应的智能超分子体系；（4）**三维结构拓展**：目前 tpy 超分子以二维平面结构为主，发展高效构建三维离散笼体系的方法仍是重要方向。随着计算辅助设计、新型表征技术（如单分子 STM 成像）以及多金属协同策略的不断完善，tpy 配位驱动自组装有望在精准纳米结构构筑和功能材料领域开创更广阔的应用前景。

## 参考文献

[1] Wang, L.; Song, B.; Khalife, S.; Li, Y.; Ming, L.-J.; Bai, S.; Xu, Y.; Yu, H.; Wang, M.; Wang, H.; Li, X. Introducing Seven Transition Metal Ions into Terpyridine-Based Supramolecules: Self-Assembly and Dynamic Ligand Exchange Study. *J. Am. Chem. Soc.* **2020**, *142*, 1811–1821. DOI: 10.1021/jacs.9b09497

[2] Zhang, Z.; Wang, H.; Wang, X.; Li, Y.; Song, B.; Bolarinwa, O.; Reese, R. A.; Zhang, T.; Wang, X.-Q.; Cai, J.; Xu, B.; Wang, M.; Liu, C.; Yang, H.-B.; Li, X. Supersnowflakes: Stepwise Self-Assembly and Dynamic Exchange of Rhombus Star-Shaped Supramolecules. *J. Am. Chem. Soc.* **2017**, *139*, 8174–8185. DOI: 10.1021/jacs.7b01326

[3] Wang, M.; Wang, C.; Hao, X.-Q.; Liu, J.; Li, X.; Xu, C.; Lopez, A.; Sun, L.; Song, M.-P.; Yang, H.-B.; Li, X. Hexagon Wreaths: Self-Assembly of Discrete Supramolecular Fractal Architectures Using Multitopic Terpyridine Ligands. *J. Am. Chem. Soc.* **2014**, *136*, 6664–6671. DOI: 10.1021/ja501417g

[4] Hwang, S.-H.; Moorefield, C. N.; Fronczek, F. R.; Lukoyanova, O.; Echegoyen, L.; Newkome, G. R. Construction of Triangular Metallomacrocycles: [M₃(1,2-bis(2,2':6',2''-terpyridin-4-yl-ethynyl)benzene)₃] [M = Ru(II), Fe(II), 2Ru(II)Fe(II)]. *Chem. Commun.* **2005**, 713–715. DOI: 10.1039/B409348H

[5] Chan, Y.-T.; Li, X.; Soler, M.; Wang, J.-L.; Wesdemiotis, C.; Newkome, G. R. Self-Assembly and Traveling Wave Ion Mobility Mass Spectrometry Analysis of Hexacadmium Macrocycles. *J. Am. Chem. Soc.* **2009**, *131*, 16395–16397. DOI: 10.1021/ja907262c

[6] Wang, J.-L.; Li, X.; Lu, X.; Hsieh, I.-F.; Cao, Y.; Moorefield, C. N.; Wesdemiotis, C.; Cheng, S. Z. D.; Newkome, G. R. Stoichiometric Self-Assembly of Shape-Persistent 2D Complexes: A Facile Route to a Symmetric Supramacromolecular Spoked Wheel. *J. Am. Chem. Soc.* **2011**, *133*, 11450–11453. DOI: 10.1021/ja203645m

[7] Schultz, A.; Li, X.; Barkakaty, B.; Moorefield, C. N.; Wesdemiotis, C.; Newkome, G. R. Stoichiometric Self-Assembly of Isomeric, Shape-Persistent, Supramacromolecular Bowtie and Butterfly Structures. *J. Am. Chem. Soc.* **2012**, *134*, 7672–7675. DOI: 10.1021/ja303177v

[8] Newkome, G. R.; Wang, P.; Moorefield, C. N.; Cho, T. J.; Mohapatra, P. P.; Li, S.; Hwang, S.-H.; Lukoyanova, O.; Echegoyen, L.; Palagallo, J. A.; Ber, V.; Durber, E. F. Nanoassembly of a Fractal Polymer: A Molecular "Sierpinski Hexagonal Gasket". *Science* **2006**, *312*, 1782–1785. DOI: 10.1126/science.1125894

[9] Sarkar, R.; Guo, K.; Moorefield, C. N.; Saunders, M. J.; Wesdemiotis, C.; Newkome, G. R. One-Step Multicomponent Self-Assembly of a First-Generation Sierpinski Triangle: From Fractal Design to Chemical Reality. *Angew. Chem. Int. Ed.* **2014**, *53*, 12182–12185. DOI: 10.1002/anie.201407285

[10] Jiang, Z.; Li, Y.; Wang, M.; Liu, D.; Yuan, J.; Chen, M.; Wang, J.; Newkome, G. R.; Sun, W.; Li, X.; Wang, P. Constructing High-Generation Sierpinski Triangles by Molecular Puzzling. *Angew. Chem. Int. Ed.* **2017**, *56*, 11450–11455. DOI: 10.1002/anie.201705480

[11] Zhang, Z.; Wang, H.; Wang, X.; Li, Y.; Song, B.; Bolarinwa, O.; Reese, R. A.; Zhang, T.; Wang, X.-Q.; Cai, J.; Xu, B.; Wang, M.; Liu, C.; Yang, H.-B.; Li, X. Supersnowflakes: Stepwise Self-Assembly and Dynamic Exchange of Rhombus Star-Shaped Supramolecules. *J. Am. Chem. Soc.* **2017**, *139*, 8174–8185. DOI: 10.1021/jacs.7b01326

[12] Zhang, Z.; Wang, H.; Shi, J.; Wang, P.; Liu, C.; Wang, M.; Li, X. Stepwise Self-Assembly and Dynamic Exchange of Supramolecular Snowflakes. *Isr. J. Chem.* **2019**, *59*, 237–247. DOI: 10.1002/ijch.201800070

[13] Jiang, Z.; Li, Y.; Wang, M.; Song, B.; Wang, K.; Sun, M.; Liu, D.; Li, X.; Yuan, J.; Chen, M.; Guo, Y.; Yang, X.; Zhang, T.; Moorefield, C. N.; Newkome, G. R.; Xu, B.; Li, X.; Wang, P. Self-Assembly of a Supramolecular Hexagram and a Supramolecular Pentagram. *Nat. Commun.* **2017**, *8*, 15476. DOI: 10.1038/ncomms15476

[14] Wang, L.; Liu, R.; Gu, J.; Song, B.; Wang, H.; Jiang, X.; Zhang, K.; Han, X.; Hao, X.-Q.; Bai, S.; Wang, M.; Li, X.; Xu, B.; Li, X. Self-Assembly of Supramolecular Fractals from Generation 1 to 5. *J. Am. Chem. Soc.* **2018**, *140*, 14087–14096. DOI: 10.1021/jacs.8b05530

[15] Wang, H.; Qian, X.; Wang, K.; Su, M.; Haoyang, W.-W.; Jiang, X.; Brzozowski, R.; Wang, M.; Gao, X.; Li, Y.; Xu, B.; Eswara, P.; Hao, X.-Q.; Gong, W.; Hou, J.-L.; Cai, J.; Li, X. Supramolecular Kandinsky Circles with High Antibacterial Activity. *Nat. Commun.* **2018**, *9*, 1815. DOI: 10.1038/s41467-018-04247-z

[16] Zhang, Z.; Li, Y.; Song, B.; Zhang, Y.; Jiang, X.; Wang, M.; Tumbleson, R.; Liu, C.; Wang, P.; Hao, X.-Q.; Rojas, T.; Ngo, A. T.; Sessler, J. L.; Newkome, G. R.; Hla, S. W.; Li, X. Intra- and Intermolecular Self-Assembly of a 20-nm-wide Supramolecular Hexagonal Grid. *Nat. Chem.* **2020**, *12*, 468–474. DOI: 10.1038/s41557-020-0454-z

[17] Wang, L.; Song, B.; Li, Y.; Gong, L.; Jiang, X.; Wang, M.; Lu, S.; Hao, X.-Q.; Xia, Z.; Zhang, Y.; Hla, S. W.; Li, X. Self-Assembly of Metallo-Supramolecules under Kinetic or Thermodynamic Control: Characterization of Positional Isomers Using Scanning Tunneling Spectroscopy. *J. Am. Chem. Soc.* **2020**, *142*, 9809–9817. DOI: 10.1021/jacs.0c03459
