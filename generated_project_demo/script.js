// 🤖 CYBORG CLICKER - Advanced Idle RPG Game Engine
console.log('🚀 CYBORG CLICKER v1.0 - Powered by AI Generation');

// Sound System
class SoundManager {
    constructor() {
        this.sounds = {
            attack: document.getElementById('attackSound'),
            upgrade: document.getElementById('upgradeSound')
        };
        this.enabled = true;
        this.volume = 0.3;
        
        // Set volume for all sounds
        Object.values(this.sounds).forEach(sound => {
            if (sound) sound.volume = this.volume;
        });
    }
    
    play(soundName) {
        if (!this.enabled) return;
        
        const sound = this.sounds[soundName];
        if (sound) {
            sound.currentTime = 0; // Reset to start
            sound.play().catch(e => {
                // Ignore errors (user interaction required)
                console.log('Sound play failed:', e);
            });
        }
    }
    
    toggle() {
        this.enabled = !this.enabled;
        return this.enabled;
    }
    
    setVolume(volume) {
        this.volume = Math.max(0, Math.min(1, volume));
        Object.values(this.sounds).forEach(sound => {
            if (sound) sound.volume = this.volume;
        });
    }
}

// Game State Management
class GameState {
    constructor() {
        this.player = {
            level: 1,
            xp: 0,
            maxXP: 100,
            damage: { min: 10, max: 15 },
            defense: 5,
            attackSpeed: 1.0,
            critChance: 5,
            credits: 0,
            energy: 100,
            nanobots: 0,
            equipment: {
                weapon: { name: 'Базовый Плазменный Меч', damage: 5 },
                armor: { name: 'Кибер-броня Mk I', defense: 3 },
                module: null
            },
            inventory: []
        };
        
        this.enemy = {
            name: 'Роботизированный Страж',
            level: 1,
            hp: 1000,
            maxHP: 1000,
            damage: { min: 5, max: 10 },
            defense: 2
        };
        
        this.upgrades = {
            damage: { level: 0, cost: 50, multiplier: 1.2 },
            speed: { level: 0, cost: 75, multiplier: 1.15 },
            autoClicker: { level: 0, cost: 200, multiplier: 1.5 },
            drones: { level: 0, cost: 500, multiplier: 2.0 }
        };
        
        this.autoSaveInterval = null;
        this.autoClickerInterval = null;
        this.energyRegenInterval = null;
        
        // Initialize sound manager
        this.soundManager = new SoundManager();
        
        this.initializeGame();
    }
    
    initializeGame() {
        this.loadGame();
        this.updateUI();
        this.startAutoSave();
        this.startEnergyRegen();
        this.generateInitialInventory();
        this.logMessage('🎮 Добро пожаловать в Cyborg Clicker!');
        this.logMessage('⚔️ Кликайте по врагам для атаки!');
        this.logMessage('💾 Игра автоматически сохраняется каждые 10 секунд');
    }
    
    // Combat System
    attack() {
        if (this.player.energy <= 0) {
            this.logMessage('⚡ Недостаточно энергии для атаки!');
            return;
        }
        
        // Calculate damage
        const baseDamage = this.randomBetween(this.player.damage.min, this.player.damage.max);
        const equipmentBonus = this.player.equipment.weapon ? this.player.equipment.weapon.damage : 0;
        const upgradeMultiplier = Math.pow(this.upgrades.damage.multiplier, this.upgrades.damage.level);
        
        let totalDamage = Math.floor((baseDamage + equipmentBonus) * upgradeMultiplier);
        
        // Critical hit check
        const isCrit = Math.random() * 100 < this.player.critChance;
        if (isCrit) {
            totalDamage = Math.floor(totalDamage * 2);
        }
        
        // Play attack sound
        this.soundManager.play('attack');
        
        // Apply damage to enemy
        this.enemy.hp -= totalDamage;
        this.player.energy -= 1;
        
        // Show damage number
        this.showDamageNumber(totalDamage, isCrit);
        
        // Check if enemy is defeated
        if (this.enemy.hp <= 0) {
            this.defeatEnemy();
        }
        
        this.updateUI();
    }
    
    defeatEnemy() {
        // Calculate rewards
        const baseXP = this.enemy.level * 25;
        const baseCredits = this.enemy.level * 10 + this.randomBetween(5, 15);
        const baseNanobots = Math.floor(this.enemy.level / 2) + this.randomBetween(0, 2);
        
        this.player.xp += baseXP;
        this.player.credits += baseCredits;
        this.player.nanobots += baseNanobots;
        
        this.logMessage(`💀 Поражен ${this.enemy.name}! Получено: ${baseXP} XP, ${baseCredits} кредитов`);
        
        // Check for level up
        this.checkLevelUp();
        
        // Drop loot chance
        if (Math.random() < 0.15) { // 15% chance
            this.dropLoot();
        }
        
        // Spawn next enemy
        this.spawnNextEnemy();
    }
    
    checkLevelUp() {
        while (this.player.xp >= this.player.maxXP) {
            this.player.xp -= this.player.maxXP;
            this.player.level++;
            this.player.maxXP = Math.floor(this.player.maxXP * 1.3);
            
            // Level up bonuses
            this.player.damage.min += 2;
            this.player.damage.max += 3;
            this.player.defense += 1;
            this.player.energy = 100; // Full energy restore
            
            this.logMessage(`🎉 УРОВЕНЬ ПОВЫШЕН! Теперь уровень ${this.player.level}`);
            this.showLevelUpEffect();
        }
    }
    
    spawnNextEnemy() {
        // Увеличиваем сложность
        const enemyLevel = Math.max(1, this.player.level - 2 + this.randomBetween(0, 4));
        
        const enemyTypes = [
            'Роботизированный Страж',
            'Кибер-Патрульный',
            'Нано-Защитник',
            'Плазменный Дрон',
            'Механический Охотник',
            'Синтетический Солдат'
        ];
        
        this.enemy = {
            name: enemyTypes[Math.floor(Math.random() * enemyTypes.length)],
            level: enemyLevel,
            hp: Math.floor(1000 * Math.pow(1.4, enemyLevel - 1)),
            maxHP: Math.floor(1000 * Math.pow(1.4, enemyLevel - 1)),
            damage: { 
                min: Math.floor(5 * Math.pow(1.2, enemyLevel - 1)), 
                max: Math.floor(10 * Math.pow(1.2, enemyLevel - 1)) 
            },
            defense: Math.floor(2 * Math.pow(1.1, enemyLevel - 1))
        };
    }
    
    // Loot System
    dropLoot() {
        const rarities = [
            { name: 'common', chance: 60, color: '#ffffff' },
            { name: 'rare', chance: 25, color: '#0080ff' },
            { name: 'epic', chance: 12, color: '#8000ff' },
            { name: 'legendary', chance: 3, color: '#ff8000' }
        ];
        
        let rarity = 'common';
        const roll = Math.random() * 100;
        let cumulative = 0;
        
        for (const r of rarities.reverse()) {
            cumulative += r.chance;
            if (roll <= cumulative) {
                rarity = r.name;
                break;
            }
        }
        
        const itemTypes = ['weapon', 'armor', 'module', 'consumable'];
        const itemType = itemTypes[Math.floor(Math.random() * itemTypes.length)];
        
        const item = this.generateItem(itemType, rarity, this.enemy.level);
        this.player.inventory.push(item);
        
        this.showLootModal(item);
        this.logMessage(`🎁 Найден предмет: ${item.name} (${rarity})`);
    }
    
    generateItem(type, rarity, level) {
        const rarityMultipliers = {
            common: 1,
            rare: 1.5,
            epic: 2.2,
            legendary: 3.5
        };
        
        const multiplier = rarityMultipliers[rarity] || 1;
        
        const items = {
            weapon: {
                names: ['Плазменный Клинок', 'Лазерная Винтовка', 'Нейро-Меч', 'Квантовый Бластер'],
                icon: '⚔️',
                stat: 'damage'
            },
            armor: {
                names: ['Нано-Броня', 'Силовой Экзоскелет', 'Энергетический Щит', 'Кибер-Костюм'],
                icon: '🛡️',
                stat: 'defense'
            },
            module: {
                names: ['Ускоритель', 'Усилитель Крита', 'Генератор Энергии', 'Нано-Процессор'],
                icon: '🔧',
                stat: 'special'
            },
            consumable: {
                names: ['Энергетический Напиток', 'Нано-Ремонтный Набор', 'Стимулятор', 'Кредит-Чип'],
                icon: '💊',
                stat: 'consumable'
            }
        };
        
        const itemTemplate = items[type];
        const baseName = itemTemplate.names[Math.floor(Math.random() * itemTemplate.names.length)];
        const name = `${baseName} Mk${level}`;
        
        let value = Math.floor(level * 10 * multiplier);
        
        return {
            id: Date.now() + Math.random(),
            name: name,
            type: type,
            rarity: rarity,
            icon: itemTemplate.icon,
            level: level,
            value: value,
            equipped: false
        };
    }
    
    // Upgrade System
    buyUpgrade(upgradeType) {
        const upgrade = this.upgrades[upgradeType];
        
        if (this.player.credits >= upgrade.cost) {
            this.player.credits -= upgrade.cost;
            upgrade.level++;
            upgrade.cost = Math.floor(upgrade.cost * 1.5);
            
            // Play upgrade sound
            this.soundManager.play('upgrade');
            
            this.logMessage(`⬆️ Улучшение '${upgradeType}' приобретено! Уровень ${upgrade.level}`);
            
            // Apply upgrade effects
            if (upgradeType === 'autoClicker' && upgrade.level === 1) {
                this.startAutoClicker();
            }
            
            this.updateUI();
        } else {
            this.logMessage(`💰 Недостаточно кредитов для улучшения '${upgradeType}'`);
        }
    }
    
    startAutoClicker() {
        if (this.autoClickerInterval) return;
        
        this.autoClickerInterval = setInterval(() => {
            if (this.upgrades.autoClicker.level > 0) {
                this.attack();
            }
        }, 2000); // Auto-attack every 2 seconds
        
        this.logMessage('🤖 Авто-кликер активирован!');
    }
    
    // Dungeon System
    enterDungeon(dungeonId) {
        if (dungeonId === 1 && this.player.level >= 5) {
            this.logMessage('🏰 Вход в Заброшенную Фабрику...');
            // Implement dungeon logic
            this.startDungeonBattle(dungeonId);
        } else if (dungeonId === 2 && this.player.level >= 15) {
            this.logMessage('🌆 Вход в Неоновые Трущобы...');
            this.startDungeonBattle(dungeonId);
        } else {
            this.logMessage('🚫 Недостаточный уровень для входа в данж!');
        }
    }
    
    startDungeonBattle(dungeonId) {
        const dungeonBosses = {
            1: { name: 'Фабричный Надзиратель', level: 8, hpMultiplier: 3 },
            2: { name: 'Неоновый Король', level: 18, hpMultiplier: 5 }
        };
        
        const boss = dungeonBosses[dungeonId];
        if (boss) {
            this.enemy = {
                name: boss.name,
                level: boss.level,
                hp: Math.floor(1000 * Math.pow(1.4, boss.level - 1) * boss.hpMultiplier),
                maxHP: Math.floor(1000 * Math.pow(1.4, boss.level - 1) * boss.hpMultiplier),
                damage: { 
                    min: Math.floor(8 * Math.pow(1.2, boss.level - 1)), 
                    max: Math.floor(15 * Math.pow(1.2, boss.level - 1)) 
                },
                defense: Math.floor(5 * Math.pow(1.1, boss.level - 1))
            };
            
            this.logMessage(`👹 Появился босс: ${boss.name}!`);
            this.updateUI();
        }
    }
    
    // Auto-save System
    startAutoSave() {
        this.autoSaveInterval = setInterval(() => {
            this.saveGame();
        }, 10000); // Save every 10 seconds
    }
    
    startEnergyRegen() {
        this.energyRegenInterval = setInterval(() => {
            if (this.player.energy < 100) {
                this.player.energy = Math.min(100, this.player.energy + 2);
                this.updateUI();
            }
        }, 3000); // Regenerate 2 energy every 3 seconds
    }
    
    saveGame() {
        const saveData = {
            player: this.player,
            enemy: this.enemy,
            upgrades: this.upgrades,
            timestamp: Date.now()
        };
        
        localStorage.setItem('cyborgClickerSave', JSON.stringify(saveData));
        this.logMessage('💾 Игра автоматически сохранена');
    }
    
    loadGame() {
        const saveData = localStorage.getItem('cyborgClickerSave');
        if (saveData) {
            try {
                const data = JSON.parse(saveData);
                
                // Calculate offline progress
                const offlineTime = Date.now() - data.timestamp;
                const offlineMinutes = Math.floor(offlineTime / 60000);
                
                if (offlineMinutes > 0) {
                    const offlineCredits = Math.floor(offlineMinutes * this.player.level * 2);
                    this.player.credits += offlineCredits;
                    this.logMessage(`🕐 Добро пожаловать! Офлайн доход: ${offlineCredits} кредитов (${offlineMinutes} мин.)`);
                }
                
                // Load saved data
                Object.assign(this.player, data.player);
                Object.assign(this.enemy, data.enemy);
                Object.assign(this.upgrades, data.upgrades);
                
                // Restart auto-clicker if purchased
                if (this.upgrades.autoClicker.level > 0) {
                    this.startAutoClicker();
                }
                
                this.logMessage('📂 Игра загружена!');
            } catch (e) {
                this.logMessage('⚠️ Ошибка загрузки сохранения, начинаем заново');
            }
        }
    }
    
    // UI Management
    updateUI() {
        // Player stats
        document.getElementById('playerLevel').textContent = this.player.level;
        document.getElementById('currentXP').textContent = this.player.xp;
        document.getElementById('maxXP').textContent = this.player.maxXP;
        document.getElementById('credits').textContent = this.player.credits.toLocaleString();
        document.getElementById('energy').textContent = this.player.energy;
        document.getElementById('nanobots').textContent = this.player.nanobots;
        
        // XP bar
        const xpPercent = (this.player.xp / this.player.maxXP) * 100;
        document.getElementById('xpBar').style.width = `${xpPercent}%`;
        
        // Player combat stats
        document.getElementById('playerDamage').textContent = `${this.player.damage.min}-${this.player.damage.max}`;
        document.getElementById('playerDefense').textContent = this.player.defense;
        document.getElementById('attackSpeed').textContent = this.player.attackSpeed.toFixed(1);
        document.getElementById('critChance').textContent = this.player.critChance;
        
        // Enemy stats
        document.getElementById('enemyName').textContent = this.enemy.name;
        document.getElementById('enemyCurrentHP').textContent = this.enemy.hp.toLocaleString();
        document.getElementById('enemyMaxHP').textContent = this.enemy.maxHP.toLocaleString();
        document.getElementById('enemyLevel').textContent = this.enemy.level;
        
        // Enemy health bar
        const healthPercent = (this.enemy.hp / this.enemy.maxHP) * 100;
        document.getElementById('enemyHealthBar').style.width = `${healthPercent}%`;
        
        // Equipment
        document.getElementById('equippedWeapon').textContent = this.player.equipment.weapon?.name || 'Нет оружия';
        document.getElementById('equippedArmor').textContent = this.player.equipment.armor?.name || 'Нет брони';
        document.getElementById('equippedModule').textContent = this.player.equipment.module?.name || 'Нет модуля';
        
        // Upgrade costs
        Object.keys(this.upgrades).forEach(key => {
            const costElement = document.getElementById(`${key}Cost`);
            if (costElement) {
                costElement.textContent = this.upgrades[key].cost;
            }
        });
        
        // Update inventory
        this.updateInventoryDisplay();
    }
    
    updateInventoryDisplay() {
        const inventoryGrid = document.getElementById('inventoryGrid');
        inventoryGrid.innerHTML = '';
        
        this.player.inventory.forEach((item, index) => {
            const itemElement = document.createElement('div');
            itemElement.className = `inventory-item ${item.rarity}`;
            itemElement.innerHTML = item.icon;
            itemElement.title = `${item.name} (${item.rarity})`;
            itemElement.onclick = () => this.useItem(index);
            inventoryGrid.appendChild(itemElement);
        });
        
        // Add empty slots
        for (let i = this.player.inventory.length; i < 30; i++) {
            const emptySlot = document.createElement('div');
            emptySlot.className = 'inventory-item empty';
            emptySlot.style.border = '1px dashed #555';
            emptySlot.style.background = 'transparent';
            inventoryGrid.appendChild(emptySlot);
        }
    }
    
    useItem(index) {
        const item = this.player.inventory[index];
        if (!item) return;
        
        if (item.type === 'consumable') {
            // Use consumable
            this.player.energy = Math.min(100, this.player.energy + 25);
            this.player.inventory.splice(index, 1);
            this.logMessage(`💊 Использован предмет: ${item.name}`);
        } else {
            // Equip item
            if (this.player.equipment[item.type]) {
                // Unequip current item back to inventory
                this.player.inventory.push(this.player.equipment[item.type]);
            }
            
            this.player.equipment[item.type] = item;
            this.player.inventory.splice(index, 1);
            this.logMessage(`⚙️ Экипирован предмет: ${item.name}`);
        }
        
        this.updateUI();
    }
    
    generateInitialInventory() {
        // Add some starting items
        this.player.inventory.push(this.generateItem('consumable', 'common', 1));
        this.player.inventory.push(this.generateItem('weapon', 'rare', 2));
    }
    
    // Visual Effects
    showDamageNumber(damage, isCrit = false) {
        const damageElement = document.createElement('div');
        damageElement.className = `damage-number ${isCrit ? 'crit-damage' : ''}`;
        damageElement.textContent = isCrit ? `КРИТ! ${damage}` : damage;
        damageElement.style.left = `${Math.random() * 100 - 50}px`;
        
        document.getElementById('damageNumbers').appendChild(damageElement);
        
        setTimeout(() => {
            damageElement.remove();
        }, 1000);
    }
    
    showLevelUpEffect() {
        const enemySprite = document.getElementById('enemySprite');
        enemySprite.style.filter = 'hue-rotate(90deg) brightness(1.5)';
        
        setTimeout(() => {
            enemySprite.style.filter = 'none';
        }, 1000);
    }
    
    showLootModal(item) {
        const modal = document.getElementById('lootModal');
        const lootContent = document.getElementById('lootContent');
        
        lootContent.innerHTML = `
            <div style="font-size: 48px; margin: 20px;">${item.icon}</div>
            <h3 style="color: ${this.getRarityColor(item.rarity)}">${item.name}</h3>
            <p>Тип: ${item.type}</p>
            <p>Редкость: ${item.rarity}</p>
            <p>Уровень: ${item.level}</p>
            <p>Характеристики: +${item.value}</p>
        `;
        
        modal.style.display = 'block';
        
        // Auto-close after 3 seconds
        setTimeout(() => {
            modal.style.display = 'none';
        }, 3000);
    }
    
    getRarityColor(rarity) {
        const colors = {
            common: '#ffffff',
            rare: '#0080ff',
            epic: '#8000ff',
            legendary: '#ff8000'
        };
        return colors[rarity] || '#ffffff';
    }
    
    // Utility functions
    randomBetween(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
    
    logMessage(message) {
        const gameLog = document.getElementById('gameLog');
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry';
        logEntry.textContent = `${new Date().toLocaleTimeString()} - ${message}`;
        
        gameLog.appendChild(logEntry);
        gameLog.scrollTop = gameLog.scrollHeight;
        
        // Keep only last 50 messages
        while (gameLog.children.length > 50) {
            gameLog.removeChild(gameLog.firstChild);
        }
    }
}

// Global Functions
let game;

function attackEnemy() {
    if (game) {
        game.attack();
    }
}

function buyUpgrade(upgradeType) {
    if (game) {
        game.buyUpgrade(upgradeType);
    }
}

function enterDungeon(dungeonId) {
    if (game) {
        game.enterDungeon(dungeonId);
    }
}

// Initialize game when page loads
document.addEventListener('DOMContentLoaded', function() {
    game = new GameState();
    
    // Close modal when clicking X or outside
    const modal = document.getElementById('lootModal');
    const closeBtn = document.querySelector('.close');
    
    closeBtn.onclick = function() {
        modal.style.display = 'none';
    }
    
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    }
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(event) {
        switch(event.key) {
            case ' ':
            case 'Enter':
                event.preventDefault();
                attackEnemy();
                break;
            case '1':
                buyUpgrade('damage');
                break;
            case '2':
                buyUpgrade('speed');
                break;
            case '3':
                buyUpgrade('autoClicker');
                break;
            case '4':
                buyUpgrade('drones');
                break;
        }
    });
    
    console.log('🎮 Cyborg Clicker полностью загружен!');
    console.log('⌨️ Горячие клавиши: Пробел/Enter - атака, 1-4 - улучшения');
});

// Export for debugging
if (typeof window !== 'undefined') {
    window.game = game;
}