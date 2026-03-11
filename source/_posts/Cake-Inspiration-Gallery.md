---
title: Cake Inspiration Gallery
date: 2026-03-09
categories:
  - Life
  - Baking
tags:
  - Cake
  - Baking
  - Inspiration
---

<style>
/* Smooth page scroll */
html { scroll-behavior: smooth; }

/* Category sections */
.cake-section {
  margin: 2em 0;
  padding: 0.8em 1.2em;
  border-left: 4px solid #f8b4c8;
  background: linear-gradient(135deg, #fff5f7 0%, #ffffff 100%);
  border-radius: 0 8px 8px 0;
}
.cake-section h2 { margin-top: 0; }

/* Gallery grid */
.cake-gallery {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  margin: 1em 0;
  align-items: start;
}

/* Each card -- scroll-unfurl on hover */
.cake-item {
  position: relative;
  overflow: hidden;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  background: #fff;
  max-height: 260px;
  transition: max-height 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94),
              box-shadow 0.3s;
  z-index: 1;
}
.cake-item:hover {
  max-height: 800px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.18);
  z-index: 10;
}

/* Image -- natural size, clipped by card */
.cake-item img {
  width: 100%;
  display: block;
  transition: filter 0.3s;
}
.cake-item:hover img {
  filter: brightness(1.05);
}

/* Reset constraints when mediumzoom opens the image */
img.medium-zoom-image--opened {
  max-height: none !important;
  object-fit: contain !important;
  border-radius: 0 !important;
}

/* Caption overlay -- rides the bottom edge as card unfurls */
.cake-item .caption {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  padding: 8px 10px;
  background: linear-gradient(transparent, rgba(0,0,0,0.65));
  color: #fff;
  font-size: 0.82em;
  line-height: 1.4;
  opacity: 0;
  transition: opacity 0.3s;
}
.cake-item:hover .caption {
  opacity: 1;
}

/* Responsive */
@media (max-width: 900px) {
  .cake-gallery { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 500px) {
  .cake-gallery { grid-template-columns: 1fr; }
}
</style>

A collection of cake inspiration shared by my friend on 2026-03-09. Each image captures a unique technique or flavor combination worth revisiting. Organized by category for easy reference.

**Quick Nav:** [IP Cakes](#1-Character-Cakes-x2F-IP卡通造型) | [Cream](#2-Cream-Techniques-x2F-奶油技法) | [Fruit](#3-Fruit-amp-Flavor-x2F-水果与口味) | [Structure](#4-Innovative-Structures-x2F-创新工艺) | [Art](#5-Artistic-Styles-x2F-艺术风格)

---

<!-- more -->

<div class="cake-section">

## 1. Character Cakes / IP卡通造型

各种可爱的卡通IP造型蛋糕，包括Jellycat系列、Sanrio角色和动物造型。

<div class="cake-gallery">
<div class="cake-item">
{% asset_img "jellycat 布丁狗.png" "Jellycat布丁狗" %}
<div class="caption">Jellycat布丁狗 -- 毛绒质感奶油造型</div>
</div>
<div class="cake-item">
{% asset_img "jellycat栗子.png" "Jellycat栗子" %}
<div class="caption">Jellycat栗子 -- 立体栗子玩偶造型</div>
</div>
<div class="cake-item">
{% asset_img "jellycat蜡烛.png" "Jellycat蜡烛" %}
<div class="caption">Jellycat蜡烛 -- 蜡烛玩偶装饰</div>
</div>
<div class="cake-item">
{% asset_img "loopy.png" "Loopy" %}
<div class="caption">Loopy -- 粉色小海狸造型</div>
</div>
<div class="cake-item">
{% asset_img "库洛米.png" "库洛米" %}
<div class="caption">库洛米 -- 经典紫黑配色</div>
</div>
<div class="cake-item">
{% asset_img "库洛米 黑色.png" "库洛米黑色" %}
<div class="caption">库洛米黑色 -- 暗黑风格版本</div>
</div>
<div class="cake-item">
{% asset_img "玉桂狗.png" "玉桂狗" %}
<div class="caption">玉桂狗 -- Sanrio经典角色</div>
</div>
<div class="cake-item">
{% asset_img "琳娜贝尔.png" "琳娜贝尔" %}
<div class="caption">琳娜贝尔 -- 迪士尼粉色小狐狸</div>
</div>
<div class="cake-item">
{% asset_img "翻糖hello kitty.png" "翻糖Hello Kitty" %}
<div class="caption">翻糖Hello Kitty -- 需要翻糖技法</div>
</div>
<div class="cake-item">
{% asset_img "奶油小狗.png" "奶油小狗" %}
<div class="caption">奶油小狗 -- 奶油裱花小狗造型</div>
</div>
<div class="cake-item">
{% asset_img "小狗蛋糕造型.png" "小狗蛋糕造型" %}
<div class="caption">小狗蛋糕造型 -- 立体小狗整体造型</div>
</div>
<div class="cake-item">
{% asset_img "栗子小狗.png" "栗子小狗" %}
<div class="caption">栗子小狗 -- 栗子色系小狗</div>
</div>
<div class="cake-item">
{% asset_img "大鹅奶油造型.png" "大鹅奶油造型" %}
<div class="caption">大鹅奶油造型 -- 立体大鹅奶油塑形</div>
</div>
</div>

</div>

---

<div class="cake-section">

## 2. Cream Techniques / 奶油技法

奶油抹面、调色、裱花等核心手法参考。

<div class="cake-gallery">
<div class="cake-item">
{% asset_img "三色奶油.png" "三色奶油" %}
<div class="caption">三色奶油 -- 三种颜色奶油分层/拼接</div>
</div>
<div class="cake-item">
{% asset_img "双层异色奶油抹面刮花.png" "双层异色奶油抹面刮花" %}
<div class="caption">双层异色奶油抹面刮花 -- 两色奶油抹面后刮出纹理</div>
</div>
<div class="cake-item">
{% asset_img "渐变奶油 抹茶撒面.png" "渐变奶油抹茶撒面" %}
<div class="caption">渐变奶油抹茶撒面 -- 奶油渐变色+抹茶粉撒面</div>
</div>
<div class="cake-item">
{% asset_img "碧螺春奶油.png" "碧螺春奶油" %}
<div class="caption">碧螺春奶油 -- 碧螺春茶粉调味奶油</div>
</div>
<div class="cake-item">
{% asset_img "龙井茶奶油.png" "龙井茶奶油" %}
<div class="caption">龙井茶奶油 -- 龙井茶风味奶油</div>
</div>
<div class="cake-item">
{% asset_img "红豆内陷 螺旋抹面.png" "红豆内馅螺旋抹面" %}
<div class="caption">红豆内馅螺旋抹面 -- 螺旋纹路抹面技法+红豆夹心</div>
</div>
<div class="cake-item">
{% asset_img "参考奶油霜造型.png" "参考奶油霜造型" %}
<div class="caption">参考奶油霜造型 -- 奶油霜造型灵感参考</div>
</div>
<div class="cake-item">
{% asset_img "蝴蝶修胚.png" "蝴蝶修胚" %}
<div class="caption">蝴蝶修胚 -- 蝴蝶造型的修胚手法</div>
</div>
</div>

</div>

---

<div class="cake-section">

## 3. Fruit & Flavor / 水果与口味

各种水果搭配与风味组合灵感。

<div class="cake-gallery">
<div class="cake-item">
{% asset_img "抹茶抱抱莓.png" "抹茶抱抱莓" %}
<div class="caption">抹茶抱抱莓 -- 抹茶+草莓的经典搭配</div>
</div>
<div class="cake-item">
{% asset_img "抹茶泰芒.png" "抹茶泰芒" %}
<div class="caption">抹茶泰芒 -- 抹茶+泰国芒果组合</div>
</div>
<div class="cake-item">
{% asset_img "杨枝甘露.png" "杨枝甘露" %}
<div class="caption">杨枝甘露 -- 经典港式甜品风味蛋糕</div>
</div>
<div class="cake-item">
{% asset_img "固体杨枝甘露.png" "固体杨枝甘露" %}
<div class="caption">固体杨枝甘露 -- 杨枝甘露的固体化呈现</div>
</div>
<div class="cake-item">
{% asset_img "泰芒了.png" "泰芒了" %}
<div class="caption">泰芒了 -- 泰式芒果风味</div>
</div>
<div class="cake-item">
{% asset_img "草莓多巴胺.png" "草莓多巴胺" %}
<div class="caption">草莓多巴胺 -- 多巴胺配色草莓蛋糕</div>
</div>
<div class="cake-item">
{% asset_img "草莓晴王（酸奶奶油）.png" "草莓晴王" %}
<div class="caption">草莓晴王 -- 草莓+晴王葡萄，酸奶奶油基底</div>
</div>
<div class="cake-item">
{% asset_img "草莓酸奶（酸奶奶油）.png" "草莓酸奶" %}
<div class="caption">草莓酸奶 -- 酸奶奶油基底的草莓蛋糕</div>
</div>
<div class="cake-item">
{% asset_img "芒果芋泥造型.png" "芒果芋泥造型" %}
<div class="caption">芒果芋泥造型 -- 芒果+芋泥双层口味</div>
</div>
<div class="cake-item">
{% asset_img "芒果血糯米.png" "芒果血糯米" %}
<div class="caption">芒果血糯米 -- 芒果搭配血糯米内馅</div>
</div>
<div class="cake-item">
{% asset_img "芝芝莓莓花.png" "芝芝莓莓花" %}
<div class="caption">芝芝莓莓花 -- 芝士+莓果+花朵装饰</div>
</div>
<div class="cake-item">
{% asset_img "蓝莓多多.png" "蓝莓多多" %}
<div class="caption">蓝莓多多 -- 蓝莓+养乐多风味</div>
</div>
<div class="cake-item">
{% asset_img "蓝莓多多巴斯克.png" "蓝莓多多巴斯克" %}
<div class="caption">蓝莓多多巴斯克 -- 蓝莓养乐多口味巴斯克</div>
</div>
<div class="cake-item">
{% asset_img "莓果巧开心.png" "莓果巧开心" %}
<div class="caption">莓果巧开心 -- 莓果+巧克力+开心果</div>
</div>
<div class="cake-item">
{% asset_img "蜜瓜夹心.png" "蜜瓜夹心" %}
<div class="caption">蜜瓜夹心 -- 蜜瓜果肉夹心</div>
</div>
<div class="cake-item">
{% asset_img "参考水果蛋糕搭配.png" "参考水果蛋糕搭配" %}
<div class="caption">参考水果蛋糕搭配 -- 水果装饰搭配参考</div>
</div>
<div class="cake-item">
{% asset_img "水果切块与装饰.png" "水果切块与装饰" %}
<div class="caption">水果切块与装饰 -- 水果切法和摆盘技巧</div>
</div>
<div class="cake-item">
{% asset_img "糯米泰椰.png" "糯米泰椰" %}
<div class="caption">糯米泰椰 -- 糯米+泰式椰浆</div>
</div>
<div class="cake-item">
{% asset_img "芭乐布蕾.png" "芭乐布蕾" %}
<div class="caption">芭乐布蕾 -- 芭乐+焦糖布蕾</div>
</div>
<div class="cake-item">
{% asset_img "芭乐酸奶巴斯克.png" "芭乐酸奶巴斯克" %}
<div class="caption">芭乐酸奶巴斯克 -- 芭乐酸奶口味巴斯克</div>
</div>
</div>

</div>

---

<div class="cake-section">

## 4. Innovative Structures / 创新工艺

结构创新、特殊工艺和材料需求。

<div class="cake-gallery">
<div class="cake-item">
{% asset_img "创新点：布丁、巴斯克夹层.png" "布丁巴斯克夹层" %}
<div class="caption">创新点：布丁、巴斯克夹层 -- 在蛋糕中嵌入布丁和巴斯克层</div>
</div>
<div class="cake-item">
{% asset_img "树莓芒果双拼巴斯克.png" "树莓芒果双拼巴斯克" %}
<div class="caption">树莓芒果双拼巴斯克 -- 双口味拼接巴斯克</div>
</div>
<div class="cake-item">
{% asset_img "杏仁挞底、开心果淋面、千层卷内馅.png" "杏仁挞底开心果淋面千层卷内馅" %}
<div class="caption">杏仁挞底+开心果淋面+千层卷内馅 -- 三重工艺叠加</div>
</div>
<div class="cake-item">
{% asset_img "巧克力脆珠和淋面.png" "巧克力脆珠和淋面" %}
<div class="caption">巧克力脆珠和淋面 -- 脆珠口感+淋面技法</div>
</div>
<div class="cake-item">
{% asset_img "碧根果贴面.png" "碧根果贴面" %}
<div class="caption">碧根果贴面 -- 碧根果片贴面装饰</div>
</div>
<div class="cake-item">
{% asset_img "异形书本.png" "异形书本" %}
<div class="caption">异形书本 -- 书本造型异形蛋糕</div>
</div>
<div class="cake-item">
{% asset_img "需要白巧克力模具.png" "需要白巧克力模具" %}
<div class="caption">需要白巧克力模具 -- 需准备白巧克力模具</div>
</div>
<div class="cake-item">
{% asset_img "需要翻糖装饰.png" "需要翻糖装饰" %}
<div class="caption">需要翻糖装饰 -- 需掌握翻糖装饰技法</div>
</div>
</div>

</div>

---

<div class="cake-section">

## 5. Artistic Styles / 艺术风格

具有艺术感的装饰风格和整体设计。

<div class="cake-gallery">
<div class="cake-item">
{% asset_img "夕阳.png" "夕阳" %}
<div class="caption">夕阳 -- 夕阳渐变色彩意境</div>
</div>
<div class="cake-item">
{% asset_img "油画玫珑.png" "油画玫珑" %}
<div class="caption">油画玫珑 -- 油画风格+玫珑瓜元素</div>
</div>
<div class="cake-item">
{% asset_img "绽放.png" "绽放" %}
<div class="caption">绽放 -- 花朵绽放造型</div>
</div>
<div class="cake-item">
{% asset_img "爱心花篮.png" "爱心花篮" %}
<div class="caption">爱心花篮 -- 爱心+花篮装饰组合</div>
</div>
<div class="cake-item">
{% asset_img "芭蕾少女-外部交叉网纹或裙边奶油装饰.png" "芭蕾少女" %}
<div class="caption">芭蕾少女 -- 外部交叉网纹或裙边奶油装饰</div>
</div>
<div class="cake-item">
{% asset_img "至臻模板.png" "至臻模板" %}
<div class="caption">至臻模板 -- 高级感模板参考</div>
</div>
</div>

</div>

---

> Thanks to my friend for sharing these wonderful cake inspirations!
