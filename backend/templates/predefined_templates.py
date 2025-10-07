from datetime import datetime
from .template_engine import TemplateEngine, TemplateMetadata, TemplateFeature, Platform, TemplateType

def create_ios_mentor_template():
    """Создает шаблон iOS AI Mentor приложения"""
    features = [
        TemplateFeature(
            name="voice_recognition",
            description="Распознавание речи через Speech Framework",
            required=True,
            dependencies=["Speech.framework", "AVFoundation.framework"],
            configuration={
                "language": "ru-RU",
                "continuous_recognition": True
            }
        ),
        TemplateFeature(
            name="text_to_speech",
            description="Синтез речи через AVSpeechSynthesizer",
            required=True,
            dependencies=["AVFoundation.framework"],
            configuration={
                "voice": "ru-RU",
                "rate": 0.5,
                "pitch": 1.0
            }
        ),
        TemplateFeature(
            name="avatar_3d",
            description="3D аватар с RealityKit",
            required=True,
            dependencies=["RealityKit.framework", "ARKit.framework"],
            configuration={
                "avatar_model": "mentor_avatar.usdz",
                "animations": ["idle", "speaking", "listening", "thinking"]
            }
        ),
        TemplateFeature(
            name="ai_integration",
            description="Интеграция с AI сервисами",
            required=True,
            dependencies=["URLSession"],
            configuration={
                "providers": ["openai", "anthropic", "localai"],
                "fallback_enabled": True
            }
        ),
        TemplateFeature(
            name="chat_history",
            description="История разговоров с CoreData",
            required=False,
            dependencies=["CoreData.framework"],
            configuration={
                "max_history_days": 30,
                "export_enabled": True
            }
        ),
        TemplateFeature(
            name="settings",
            description="Настройки приложения",
            required=True,
            dependencies=["SwiftUI"],
            configuration={
                "themes": ["light", "dark", "auto"],
                "languages": ["ru", "en"]
            }
        )
    ]
    
    template_files = {
        "ContentView.swift": """
import SwiftUI
import Speech
import AVFoundation
import RealityKit

struct ContentView: View {
    @StateObject private var voiceRecognizer = VoiceRecognizer()
    @StateObject private var aiService = AIService()
    @StateObject private var avatarController = AvatarController()
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // Фон
                LinearGradient(
                    colors: [Color.blue.opacity(0.1), Color.purple.opacity(0.1)],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()
                
                VStack(spacing: 20) {
                    // 3D Аватар
                    Avatar3DView(controller: avatarController)
                        .frame(height: geometry.size.height * 0.4)
                        .clipShape(RoundedRectangle(cornerRadius: 20))
                    
                    // Статус
                    Text(aiService.status)
                        .font(.title2)
                        .foregroundColor(.primary)
                    
                    // Область чата
                    ScrollViewReader { proxy in
                        ScrollView {
                            LazyVStack(alignment: .leading, spacing: 12) {
                                ForEach(aiService.messages) { message in
                                    MessageBubble(message: message)
                                }
                            }
                            .padding()
                        }
                        .frame(maxHeight: geometry.size.height * 0.3)
                        .onChange(of: aiService.messages.count) { _ in
                            if let lastMessage = aiService.messages.last {
                                proxy.scrollTo(lastMessage.id, anchor: .bottom)
                            }
                        }
                    }
                    
                    // Кнопки управления
                    HStack(spacing: 20) {
                        Button(action: {
                            if voiceRecognizer.isRecording {
                                voiceRecognizer.stopRecording()
                            } else {
                                voiceRecognizer.startRecording()
                            }
                        }) {
                            Image(systemName: voiceRecognizer.isRecording ? "stop.circle.fill" : "mic.circle.fill")
                                .font(.system(size: 50))
                                .foregroundColor(voiceRecognizer.isRecording ? .red : .blue)
                        }
                        
                        Button("Очистить") {
                            aiService.clearHistory()
                        }
                        .padding()
                        .background(Color.gray.opacity(0.2))
                        .cornerRadius(10)
                        
                        NavigationLink(destination: SettingsView()) {
                            Image(systemName: "gear")
                                .font(.system(size: 24))
                                .foregroundColor(.primary)
                        }
                    }
                    .padding()
                }
            }
        }
        .navigationTitle("{{project_name}}")
        .onReceive(voiceRecognizer.$recognizedText) { text in
            if !text.isEmpty {
                aiService.sendMessage(text)
                avatarController.playAnimation(.listening)
            }
        }
        .onReceive(aiService.$currentResponse) { response in
            if !response.isEmpty {
                avatarController.playAnimation(.speaking)
            }
        }
    }
}
""",
        
        "VoiceRecognizer.swift": """
import Speech
import AVFoundation
import SwiftUI

class VoiceRecognizer: ObservableObject {
    @Published var recognizedText = ""
    @Published var isRecording = false
    
    private let speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "ru-RU"))
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private var recognitionTask: SFSpeechRecognitionTask?
    private let audioEngine = AVAudioEngine()
    
    init() {
        requestPermissions()
    }
    
    func requestPermissions() {
        SFSpeechRecognizer.requestAuthorization { status in
            DispatchQueue.main.async {
                // Handle authorization
            }
        }
        
        AVAudioSession.sharedInstance().requestRecordPermission { granted in
            // Handle permission
        }
    }
    
    func startRecording() {
        guard let speechRecognizer = speechRecognizer,
              speechRecognizer.isAvailable else { return }
        
        try? AVAudioSession.sharedInstance().setCategory(.record, mode: .measurement, options: .duckOthers)
        try? AVAudioSession.sharedInstance().setActive(true, options: .notifyOthersOnDeactivation)
        
        recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        guard let recognitionRequest = recognitionRequest else { return }
        
        recognitionRequest.shouldReportPartialResults = true
        
        let inputNode = audioEngine.inputNode
        let recordingFormat = inputNode.outputFormat(forBus: 0)
        
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { buffer, _ in
            recognitionRequest.append(buffer)
        }
        
        recognitionTask = speechRecognizer.recognitionTask(with: recognitionRequest) { result, error in
            DispatchQueue.main.async {
                if let result = result {
                    self.recognizedText = result.bestTranscription.formattedString
                    
                    if result.isFinal {
                        self.stopRecording()
                    }
                }
            }
        }
        
        audioEngine.prepare()
        try? audioEngine.start()
        isRecording = true
    }
    
    func stopRecording() {
        audioEngine.stop()
        audioEngine.inputNode.removeTap(onBus: 0)
        
        recognitionRequest?.endAudio()
        recognitionTask?.cancel()
        
        recognitionRequest = nil
        recognitionTask = nil
        isRecording = false
    }
}
""",
        
        "Avatar3DView.swift": """
import SwiftUI
import RealityKit
import ARKit

struct Avatar3DView: UIViewRepresentable {
    let controller: AvatarController
    
    func makeUIView(context: Context) -> ARView {
        let arView = ARView(frame: .zero)
        
        // Загружаем 3D модель аватара
        if let avatarEntity = try? Entity.loadModel(named: "{{avatar_model}}") {
            let anchor = AnchorEntity(world: [0, 0, -0.5])
            anchor.addChild(avatarEntity)
            arView.scene.addAnchor(anchor)
            
            controller.avatarEntity = avatarEntity
        }
        
        return arView
    }
    
    func updateUIView(_ uiView: ARView, context: Context) {
        // Обновления если нужны
    }
}

class AvatarController: ObservableObject {
    var avatarEntity: Entity?
    
    enum AnimationType {
        case idle, speaking, listening, thinking
    }
    
    func playAnimation(_ type: AnimationType) {
        guard let entity = avatarEntity else { return }
        
        let animationName = switch type {
        case .idle: "idle"
        case .speaking: "speaking"
        case .listening: "listening"
        case .thinking: "thinking"
        }
        
        // Проигрываем анимацию
        if let animation = entity.availableAnimations.first(where: { $0.name == animationName }) {
            entity.playAnimation(animation.repeat())
        }
    }
}
""",
        
        "AIService.swift": """
import Foundation
import SwiftUI

struct ChatMessage: Identifiable {
    let id = UUID()
    let text: String
    let isUser: Bool
    let timestamp: Date
}

class AIService: ObservableObject {
    @Published var messages: [ChatMessage] = []
    @Published var status = "Готов к общению"
    @Published var currentResponse = ""
    
    private let aiProviders = ["{{ai_provider_primary}}", "{{ai_provider_fallback}}"]
    
    func sendMessage(_ text: String) {
        let userMessage = ChatMessage(text: text, isUser: true, timestamp: Date())
        messages.append(userMessage)
        
        status = "Думаю..."
        
        Task {
            let response = await generateResponse(for: text)
            
            DispatchQueue.main.async {
                let aiMessage = ChatMessage(text: response, isUser: false, timestamp: Date())
                self.messages.append(aiMessage)
                self.status = "Готов к общению"
                self.currentResponse = response
                
                // Озвучиваем ответ
                self.speakText(response)
            }
        }
    }
    
    private func generateResponse(for prompt: String) async -> String {
        // Здесь будет интеграция с AI API
        // Пока возвращаем тестовый ответ
        return "Это ответ AI на ваш вопрос: \\(prompt)"
    }
    
    private func speakText(_ text: String) {
        // TTS реализация
    }
    
    func clearHistory() {
        messages.removeAll()
        currentResponse = ""
    }
}
""",
        
        "SettingsView.swift": """
import SwiftUI

struct SettingsView: View {
    @AppStorage("selectedTheme") private var selectedTheme = "auto"
    @AppStorage("selectedLanguage") private var selectedLanguage = "ru"
    @AppStorage("voiceRate") private var voiceRate = 0.5
    @AppStorage("enableHaptics") private var enableHaptics = true
    
    var body: some View {
        NavigationView {
            List {
                Section("Внешний вид") {
                    Picker("Тема", selection: $selectedTheme) {
                        Text("Светлая").tag("light")
                        Text("Темная").tag("dark")
                        Text("Системная").tag("auto")
                    }
                }
                
                Section("Язык и голос") {
                    Picker("Язык", selection: $selectedLanguage) {
                        Text("Русский").tag("ru")
                        Text("English").tag("en")
                    }
                    
                    VStack(alignment: .leading) {
                        Text("Скорость речи")
                        Slider(value: $voiceRate, in: 0.1...1.0, step: 0.1)
                    }
                }
                
                Section("Взаимодействие") {
                    Toggle("Вибрация", isOn: $enableHaptics)
                }
                
                Section("О приложении") {
                    HStack {
                        Text("Версия")
                        Spacer()
                        Text("{{app_version}}")
                    }
                    
                    HStack {
                        Text("AI Модель")
                        Spacer()
                        Text("{{ai_model}}")
                    }
                }
            }
            .navigationTitle("Настройки")
        }
    }
}
""",
        
        "Info.plist": """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>$(DEVELOPMENT_LANGUAGE)</string>
    <key>CFBundleDisplayName</key>
    <string>{{project_name}}</string>
    <key>CFBundleExecutable</key>
    <string>$(EXECUTABLE_NAME)</string>
    <key>CFBundleIdentifier</key>
    <string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>$(PRODUCT_NAME)</string>
    <key>CFBundlePackageType</key>
    <string>$(PRODUCT_BUNDLE_PACKAGE_TYPE)</string>
    <key>CFBundleShortVersionString</key>
    <string>{{app_version}}</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>NSMicrophoneUsageDescription</key>
    <string>Приложению нужен доступ к микрофону для распознавания речи</string>
    <key>NSSpeechRecognitionUsageDescription</key>
    <string>Приложению нужен доступ к распознаванию речи для общения с AI</string>
    <key>NSCameraUsageDescription</key>
    <string>Приложению нужен доступ к камере для AR функций</string>
    <key>UILaunchScreen</key>
    <dict/>
    <key>UIRequiredDeviceCapabilities</key>
    <array>
        <string>armv7</string>
        <string>arkit</string>
    </array>
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
        <string>UIInterfaceOrientationLandscapeLeft</string>
        <string>UIInterfaceOrientationLandscapeRight</string>
    </array>
</dict>
</plist>"""
    }
    
    template_data = {
        "template_id": "ios_mentor_v1",
        "name": "iOS AI Mentor App",
        "description": "Полноценное iOS приложение AI наставника с 3D аватаром, голосовым управлением и продвинутой интеграцией с AI сервисами",
        "version": "1.0.0",
        "platform": "ios",
        "template_type": "ios_mentor",
        "author": "Lovable AI Platform",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "tags": ["ai", "mentor", "3d-avatar", "voice", "swiftui", "realitykit"],
        "features": [asdict(feature) for feature in features],
        "requirements": {
            "ios_version": "15.0+",
            "xcode_version": "13.0+",
            "frameworks": ["SwiftUI", "RealityKit", "ARKit", "Speech", "AVFoundation", "CoreData"],
            "devices": ["iPhone", "iPad"]
        },
        "examples": [
            {
                "name": "Простой AI наставник",
                "description": "Базовое приложение с голосовым чатом",
                "variables": {
                    "project_name": "MyAIMentor",
                    "app_version": "1.0",
                    "ai_provider_primary": "openai",
                    "ai_provider_fallback": "localai",
                    "avatar_model": "default_avatar.usdz",
                    "ai_model": "GPT-4"
                }
            }
        ]
    }
    
    return template_data, template_files

def create_android_mentor_template():
    """Создает шаблон Android AI Mentor приложения"""
    features = [
        TemplateFeature(
            name="voice_recognition",
            description="Распознавание речи через SpeechRecognizer",
            required=True,
            dependencies=["android.speech"],
            configuration={
                "language": "ru-RU",
                "continuous_recognition": True
            }
        ),
        TemplateFeature(
            name="text_to_speech",
            description="Синтез речи через TextToSpeech",
            required=True,
            dependencies=["android.speech.tts"],
            configuration={
                "language": "ru-RU",
                "speed": 1.0
            }
        ),
        TemplateFeature(
            name="avatar_3d",
            description="3D аватар с Filament/SceneForm",
            required=True,
            dependencies=["com.google.ar.sceneform"],
            configuration={
                "avatar_model": "mentor_avatar.glb",
                "animations": ["idle", "speaking", "listening"]
            }
        )
    ]
    
    template_files = {
        "MainActivity.kt": """
package com.{{package_name}}

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.{{package_name}}.ui.theme.{{ProjectName}}Theme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            {{ProjectName}}Theme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    MentorScreen()
                }
            }
        }
    }
}

@Composable
fun MentorScreen() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "{{project_name}}",
            style = MaterialTheme.typography.headlineMedium
        )
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // 3D Avatar будет здесь
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .height(300.dp),
            elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
        ) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                Text("3D Avatar")
            }
        }
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // Кнопки управления
        Row(
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Button(
                onClick = { /* Start recording */ },
                modifier = Modifier.weight(1f)
            ) {
                Text("Говорить")
            }
            
            Button(
                onClick = { /* Clear chat */ },
                modifier = Modifier.weight(1f)
            ) {
                Text("Очистить")
            }
        }
    }
}
""",
        
        "AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    package="com.{{package_name}}">

    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.CAMERA" />
    
    <uses-feature
        android:name="android.hardware.camera.ar"
        android:required="true" />

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="{{project_name}}"
        android:theme="@style/Theme.{{ProjectName}}"
        tools:targetApi="31">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.{{ProjectName}}">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        
    </application>
</manifest>"""
    }
    
    template_data = {
        "template_id": "android_mentor_v1",
        "name": "Android AI Mentor App",
        "description": "Android приложение AI наставника с голосовым управлением и 3D аватаром на Jetpack Compose",
        "version": "1.0.0",
        "platform": "android",
        "template_type": "android_mentor",
        "author": "Lovable AI Platform",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "tags": ["ai", "mentor", "3d-avatar", "voice", "jetpack-compose", "kotlin"],
        "features": [asdict(feature) for feature in features],
        "requirements": {
            "android_version": "API 26+",
            "gradle_version": "8.0+",
            "kotlin_version": "1.8+",
            "compose_version": "1.5+"
        },
        "examples": [
            {
                "name": "Базовый Android наставник",
                "description": "Простое приложение с голосовым чатом",
                "variables": {
                    "project_name": "AI Mentor",
                    "package_name": "aimentor",
                    "ProjectName": "AIMentor"
                }
            }
        ]
    }
    
    return template_data, template_files

def setup_predefined_templates(engine: TemplateEngine):
    """Создает все предустановленные шаблоны"""
    
    # iOS AI Mentor
    ios_template_data, ios_template_files = create_ios_mentor_template()
    result = engine.create_custom_template(ios_template_data, ios_template_files)
    if result["success"]:
        print(f"Created iOS Mentor template: {result['template_id']}")
    
    # Android AI Mentor
    android_template_data, android_template_files = create_android_mentor_template()
    result = engine.create_custom_template(android_template_data, android_template_files)
    if result["success"]:
        print(f"Created Android Mentor template: {result['template_id']}")

# Функция для быстрого создания всех шаблонов
def initialize_all_templates():
    """Инициализирует все предустановленные шаблоны"""
    from .template_engine import template_engine
    setup_predefined_templates(template_engine)
    print("All predefined templates initialized successfully!")

if __name__ == "__main__":
    initialize_all_templates()