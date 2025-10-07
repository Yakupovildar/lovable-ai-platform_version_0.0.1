#!/usr/bin/env python3
"""
MOBILE PROJECT GENERATORS
Система генерации нативных мобильных приложений для iOS и Android
"""

import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import base64

class MobileProjectGenerator:
    """Генератор мобильных проектов с полной поддержкой iOS и Android"""
    
    def __init__(self):
        self.platforms = {
            'ios': {
                'language': 'swift',
                'framework': 'swiftui',
                'build_system': 'xcode',
                'dependencies': 'spm',  # Swift Package Manager
                'min_version': '15.0'
            },
            'android': {
                'language': 'kotlin',
                'framework': 'jetpack_compose',
                'build_system': 'gradle',
                'dependencies': 'gradle',
                'min_version': '24'
            },
            'react_native': {
                'framework': 'react_native',
                'language': 'typescript',
                'build_system': 'metro',
                'dependencies': 'npm'
            }
        }
        
    def generate_ios_mentor_app(self, app_name: str, features: List[str]) -> Dict[str, str]:
        """Создает полный iOS проект AI наставника с 3D и голосом"""
        
        project_id = str(uuid.uuid4())
        bundle_id = f"com.aimentor.{app_name.lower().replace(' ', '')}"
        
        return {
            # ОСНОВНОЙ ПРОЕКТ
            f'{app_name}.xcodeproj/project.pbxproj': self._generate_xcode_project(app_name, bundle_id),
            
            # SWIFT UI ИНТЕРФЕЙС
            f'{app_name}/ContentView.swift': self._generate_main_content_view(app_name, features),
            f'{app_name}/MentorSelectionView.swift': self._generate_mentor_selection_view(),
            f'{app_name}/ChatView.swift': self._generate_chat_view(),
            f'{app_name}/Avatar3DView.swift': self._generate_3d_avatar_view(),
            
            # AI И ГОЛОСОВЫЕ МОДУЛИ
            f'{app_name}/MentorViewModel.swift': self._generate_ai_mentor_viewmodel(),
            f'{app_name}/VoiceRecognizer.swift': self._generate_voice_recognition(),
            f'{app_name}/SpeechSynthesizer.swift': self._generate_text_to_speech(),
            f'{app_name}/AudioManager.swift': self._generate_audio_manager(),
            
            # МОДЕЛИ ДАННЫХ
            f'{app_name}/Models/MentorModel.swift': self._generate_mentor_model(),
            f'{app_name}/Models/MessageModel.swift': self._generate_message_model(),
            f'{app_name}/Models/VoiceSettings.swift': self._generate_voice_settings(),
            
            # 3D И АНИМАЦИИ
            f'{app_name}/3D/Avatar3DRenderer.swift': self._generate_3d_renderer(),
            f'{app_name}/3D/FaceAnimator.swift': self._generate_face_animator(),
            f'{app_name}/3D/EmotionEngine.swift': self._generate_emotion_engine(),
            
            # СЕТЕВЫЕ МОДУЛИ
            f'{app_name}/Network/AIService.swift': self._generate_ai_service(),
            f'{app_name}/Network/VoiceService.swift': self._generate_voice_service(),
            f'{app_name}/Network/MentorDataLoader.swift': self._generate_mentor_data_loader(),
            
            # КОНФИГУРАЦИЯ И МЕТАДАННЫЕ
            f'{app_name}/Info.plist': self._generate_info_plist(app_name, bundle_id),
            'Package.swift': self._generate_spm_dependencies(features),
            'README.md': self._generate_ios_readme(app_name, features),
            
            # РЕСУРСЫ
            f'{app_name}/Assets.xcassets/AppIcon.appiconset/Contents.json': self._generate_app_icon_config(),
            f'{app_name}/Localizable.strings': self._generate_russian_localization(),
        }
    
    def _generate_main_content_view(self, app_name: str, features: List[str]) -> str:
        """Генерирует главный экран SwiftUI с полным функционалом"""
        return f'''import SwiftUI
import RealityKit
import Speech
import AVFoundation

struct ContentView: View {{
    @StateObject private var mentorViewModel = MentorViewModel()
    @StateObject private var voiceRecognizer = VoiceRecognizer()
    @StateObject private var speechSynthesizer = SpeechSynthesizer()
    @State private var selectedMentor: MentorModel? = nil
    @State private var showMentorSelection = false
    
    var body: some View {{
        NavigationView {{
            ZStack {{
                // Градиентный фон
                LinearGradient(
                    gradient: Gradient(colors: [.purple.opacity(0.8), .blue.opacity(0.6)]),
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()
                
                VStack(spacing: 30) {{
                    // Заголовок
                    VStack {{
                        Text("🧠 {app_name}")
                            .font(.largeTitle)
                            .fontWeight(.bold)
                            .foregroundColor(.white)
                        
                        Text("Получите персональные советы от миллиардеров")
                            .font(.headline)
                            .foregroundColor(.white.opacity(0.8))
                            .multilineTextAlignment(.center)
                    }}
                    .padding(.top, 50)
                    
                    // 3D Превью наставника
                    if let mentor = selectedMentor {{
                        Avatar3DView(mentor: mentor)
                            .frame(width: 200, height: 200)
                            .clipShape(Circle())
                            .shadow(radius: 20)
                    }} else {{
                        Circle()
                            .fill(.white.opacity(0.2))
                            .frame(width: 200, height: 200)
                            .overlay(
                                Image(systemName: "person.3.sequence.fill")
                                    .font(.system(size: 60))
                                    .foregroundColor(.white.opacity(0.7))
                            )
                    }}
                    
                    // Кнопки управления
                    VStack(spacing: 20) {{
                        Button(action: {{
                            showMentorSelection = true
                        }}) {{
                            HStack {{
                                Image(systemName: "person.crop.square.filled.and.at.rectangle")
                                Text("Выбрать наставника")
                            }}
                            .font(.headline)
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .frame(height: 55)
                            .background(.ultraThinMaterial)
                            .clipShape(RoundedRectangle(cornerRadius: 15))
                        }}
                        
                        if selectedMentor != nil {{
                            NavigationLink(destination: ChatView(mentor: selectedMentor!, 
                                                                voiceRecognizer: voiceRecognizer,
                                                                speechSynthesizer: speechSynthesizer)) {{
                                HStack {{
                                    Image(systemName: "message.circle.fill")
                                    Text("Начать общение")
                                }}
                                .font(.headline)
                                .foregroundColor(.white)
                                .frame(maxWidth: .infinity)
                                .frame(height: 55)
                                .background(.green.opacity(0.7))
                                .clipShape(RoundedRectangle(cornerRadius: 15))
                            }}
                        }}
                    }}
                    .padding(.horizontal, 30)
                    
                    Spacer()
                    
                    // Статус и настройки
                    HStack {{
                        VStack {{
                            Image(systemName: voiceRecognizer.isAvailable ? "checkmark.circle.fill" : "xmark.circle.fill")
                                .foregroundColor(voiceRecognizer.isAvailable ? .green : .red)
                            Text("Голос")
                                .font(.caption)
                                .foregroundColor(.white.opacity(0.7))
                        }}
                        
                        Spacer()
                        
                        VStack {{
                            Image(systemName: mentorViewModel.isAIReady ? "brain.head.profile" : "brain.head.profile.fill")
                                .foregroundColor(mentorViewModel.isAIReady ? .green : .orange)
                            Text("ИИ")
                                .font(.caption)
                                .foregroundColor(.white.opacity(0.7))
                        }}
                        
                        Spacer()
                        
                        VStack {{
                            Image(systemName: "cube.transparent")
                                .foregroundColor(.blue)
                            Text("3D")
                                .font(.caption)
                                .foregroundColor(.white.opacity(0.7))
                        }}
                    }}
                    .padding(.horizontal, 40)
                    .padding(.bottom, 30)
                }}
            }}
        }}
        .sheet(isPresented: $showMentorSelection) {{
            MentorSelectionView(selectedMentor: $selectedMentor)
        }}
        .onAppear {{
            requestPermissions()
            mentorViewModel.initialize()
        }}
    }}
    
    private func requestPermissions() {{
        SFSpeechRecognizer.requestAuthorization {{ status in
            DispatchQueue.main.async {{
                voiceRecognizer.authorizationStatus = status
            }}
        }}
        
        AVAudioSession.sharedInstance().requestRecordPermission {{ granted in
            DispatchQueue.main.async {{
                voiceRecognizer.hasAudioPermission = granted
            }}
        }}
    }}
}}

#Preview {{
    ContentView()
}}
'''
    
    def _generate_voice_recognition(self) -> str:
        """Генерирует полнофункциональный модуль распознавания речи"""
        return '''import Speech
import AVFoundation
import Combine

@MainActor
class VoiceRecognizer: ObservableObject {
    private let speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "ru-RU"))!
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private var recognitionTask: SFSpeechRecognitionTask?
    private let audioEngine = AVAudioEngine()
    
    @Published var recognizedText = ""
    @Published var isRecording = false
    @Published var isAvailable = false
    @Published var authorizationStatus: SFSpeechRecognizerAuthorizationStatus = .notDetermined
    @Published var hasAudioPermission = false
    
    private var audioSession: AVAudioSession {
        AVAudioSession.sharedInstance()
    }
    
    init() {
        setupSpeechRecognizer()
    }
    
    private func setupSpeechRecognizer() {
        speechRecognizer.delegate = self
        isAvailable = speechRecognizer.isAvailable && hasAudioPermission
    }
    
    func startRecording() async throws {
        guard !isRecording else { return }
        
        // Настраиваем аудиосессию
        try audioSession.setCategory(.record, mode: .measurement, options: .duckOthers)
        try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
        
        // Останавливаем текущую задачу
        recognitionTask?.cancel()
        recognitionTask = nil
        
        // Создаем новый запрос
        recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        guard let recognitionRequest = recognitionRequest else {
            throw VoiceRecognitionError.requestCreationFailed
        }
        
        recognitionRequest.shouldReportPartialResults = true
        
        // Настраиваем аудиодвижок
        let inputNode = audioEngine.inputNode
        let recordingFormat = inputNode.outputFormat(forBus: 0)
        
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { buffer, _ in
            recognitionRequest.append(buffer)
        }
        
        audioEngine.prepare()
        try audioEngine.start()
        
        isRecording = true
        recognizedText = ""
        
        // Начинаем распознавание
        recognitionTask = speechRecognizer.recognitionTask(with: recognitionRequest) { [weak self] result, error in
            guard let self = self else { return }
            
            if let result = result {
                DispatchQueue.main.async {
                    self.recognizedText = result.bestTranscription.formattedString
                }
            }
            
            if error != nil || (result?.isFinal ?? false) {
                DispatchQueue.main.async {
                    self.stopRecording()
                }
            }
        }
    }
    
    func stopRecording() {
        guard isRecording else { return }
        
        audioEngine.stop()
        audioEngine.inputNode.removeTap(onBus: 0)
        recognitionRequest?.endAudio()
        recognitionTask?.cancel()
        
        recognitionRequest = nil
        recognitionTask = nil
        isRecording = false
        
        try? audioSession.setActive(false)
    }
    
    func toggleRecording() async {
        if isRecording {
            stopRecording()
        } else {
            do {
                try await startRecording()
            } catch {
                print("Ошибка начала записи: \\(error.localizedDescription)")
            }
        }
    }
}

extension VoiceRecognizer: SFSpeechRecognizerDelegate {
    func speechRecognizer(_ speechRecognizer: SFSpeechRecognizer, availabilityDidChange available: Bool) {
        isAvailable = available && hasAudioPermission
    }
}

enum VoiceRecognitionError: Error, LocalizedError {
    case requestCreationFailed
    case audioEngineError
    case permissionDenied
    
    var errorDescription: String? {
        switch self {
        case .requestCreationFailed:
            return "Не удалось создать запрос на распознавание речи"
        case .audioEngineError:
            return "Ошибка аудиодвижка"
        case .permissionDenied:
            return "Нет разрешения на использование микрофона"
        }
    }
}
'''

    def _generate_text_to_speech(self) -> str:
        """Генерирует модуль синтеза речи с реалистичными голосами"""
        return '''import AVFoundation
import Combine

@MainActor
class SpeechSynthesizer: ObservableObject {
    private let synthesizer = AVSpeechSynthesizer()
    
    @Published var isSpeaking = false
    @Published var currentText = ""
    @Published var speechRate: Float = 0.5
    @Published var speechPitch: Float = 1.0
    @Published var speechVolume: Float = 1.0
    
    // Голоса наставников (эмуляция)
    private let mentorVoices: [String: String] = [
        "elon_musk": "ru-RU",
        "bill_gates": "ru-RU", 
        "jeff_bezos": "ru-RU",
        "warren_buffett": "ru-RU"
    ]
    
    init() {
        synthesizer.delegate = self
    }
    
    func speak(_ text: String, mentor: String = "elon_musk") {
        // Останавливаем текущую речь
        if synthesizer.isSpeaking {
            synthesizer.stopSpeaking(at: .immediate)
        }
        
        let utterance = AVSpeechUtterance(string: text)
        
        // Настраиваем голос для наставника
        let voiceLanguage = mentorVoices[mentor] ?? "ru-RU"
        utterance.voice = AVSpeechSynthesisVoice(language: voiceLanguage)
        
        // Настраиваем параметры голоса в зависимости от наставника
        switch mentor {
        case "elon_musk":
            utterance.rate = 0.55
            utterance.pitchMultiplier = 1.1
            utterance.volume = 0.9
        case "bill_gates":
            utterance.rate = 0.45
            utterance.pitchMultiplier = 0.95
            utterance.volume = 0.85
        case "jeff_bezos":
            utterance.rate = 0.5
            utterance.pitchMultiplier = 0.9
            utterance.volume = 0.9
        case "warren_buffett":
            utterance.rate = 0.4
            utterance.pitchMultiplier = 0.85
            utterance.volume = 0.8
        default:
            utterance.rate = speechRate
            utterance.pitchMultiplier = speechPitch
            utterance.volume = speechVolume
        }
        
        currentText = text
        synthesizer.speak(utterance)
    }
    
    func stop() {
        synthesizer.stopSpeaking(at: .immediate)
        isSpeaking = false
        currentText = ""
    }
    
    func pause() {
        synthesizer.pauseSpeaking(at: .immediate)
    }
    
    func resume() {
        synthesizer.continueSpeaking()
    }
}

extension SpeechSynthesizer: AVSpeechSynthesizerDelegate {
    func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didStart utterance: AVSpeechUtterance) {
        isSpeaking = true
    }
    
    func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didFinish utterance: AVSpeechUtterance) {
        isSpeaking = false
        currentText = ""
    }
    
    func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didCancel utterance: AVSpeechUtterance) {
        isSpeaking = false
        currentText = ""
    }
}
'''

    def _generate_3d_avatar_view(self) -> str:
        """Генерирует 3D аватар с анимациями"""
        return '''import SwiftUI
import RealityKit
import Combine

struct Avatar3DView: UIViewRepresentable {
    let mentor: MentorModel
    @State private var arView: ARView?
    @StateObject private var emotionEngine = EmotionEngine()
    
    func makeUIView(context: Context) -> ARView {
        let arView = ARView(frame: .zero)
        self.arView = arView
        
        // Создаем 3D сцену
        setupScene(arView)
        
        return arView
    }
    
    func updateUIView(_ uiView: ARView, context: Context) {
        // Обновляем анимации при изменении эмоций
        updateAvatarEmotion(uiView)
    }
    
    private func setupScene(_ arView: ARView) {
        // Создаем якорь для 3D модели
        let anchor = AnchorEntity()
        
        // Загружаем 3D модель головы наставника
        let avatarEntity = createAvatarEntity(for: mentor)
        anchor.addChild(avatarEntity)
        
        // Добавляем освещение
        let lightEntity = DirectionalLight()
        lightEntity.light.intensity = 2000
        lightEntity.position = [0, 1, 1]
        anchor.addChild(lightEntity)
        
        // Добавляем в сцену
        arView.scene.addAnchor(anchor)
        
        // Настраиваем камеру
        arView.cameraMode = .nonAR
    }
    
    private func createAvatarEntity(for mentor: MentorModel) -> Entity {
        // В реальном приложении здесь бы загружалась 3D модель
        let entity = Entity()
        
        // Создаем базовую геометрию головы
        let headMesh = MeshResource.generateSphere(radius: 0.15)
        let headMaterial = createMentorMaterial(for: mentor)
        let headEntity = ModelEntity(mesh: headMesh, materials: [headMaterial])
        
        // Создаем глаза
        let eyeMesh = MeshResource.generateSphere(radius: 0.02)
        let eyeMaterial = SimpleMaterial(color: .white, isMetallic: false)
        
        let leftEye = ModelEntity(mesh: eyeMesh, materials: [eyeMaterial])
        leftEye.position = [-0.05, 0.05, 0.12]
        
        let rightEye = ModelEntity(mesh: eyeMesh, materials: [eyeMaterial])
        rightEye.position = [0.05, 0.05, 0.12]
        
        // Создаем рот
        let mouthMesh = MeshResource.generateBox(width: 0.06, height: 0.02, depth: 0.01)
        let mouthMaterial = SimpleMaterial(color: .red, isMetallic: false)
        let mouth = ModelEntity(mesh: mouthMesh, materials: [mouthMaterial])
        mouth.position = [0, -0.05, 0.12]
        
        entity.addChild(headEntity)
        entity.addChild(leftEye)
        entity.addChild(rightEye)
        entity.addChild(mouth)
        
        // Добавляем компонент анимации
        let animationComponent = AvatarAnimationComponent()
        entity.components.set(animationComponent)
        
        return entity
    }
    
    private func createMentorMaterial(for mentor: MentorModel) -> Material {
        var material = SimpleMaterial()
        
        switch mentor.id {
        case "elon_musk":
            material.color = .init(tint: .init(red: 0.9, green: 0.8, blue: 0.7, alpha: 1.0))
        case "bill_gates":
            material.color = .init(tint: .init(red: 0.95, green: 0.85, blue: 0.75, alpha: 1.0))
        case "jeff_bezos":
            material.color = .init(tint: .init(red: 0.85, green: 0.75, blue: 0.65, alpha: 1.0))
        case "warren_buffett":
            material.color = .init(tint: .init(red: 0.95, green: 0.9, blue: 0.8, alpha: 1.0))
        default:
            material.color = .init(tint: .gray)
        }
        
        return material
    }
    
    private func updateAvatarEmotion(_ arView: ARView) {
        // Обновляем анимации лица на основе текущей эмоции
        guard let anchor = arView.scene.anchors.first else { return }
        
        let currentEmotion = emotionEngine.currentEmotion
        applyEmotionAnimation(to: anchor, emotion: currentEmotion)
    }
    
    private func applyEmotionAnimation(to anchor: AnchorEntity, emotion: EmotionType) {
        // Применяем анимации в зависимости от эмоции
        let duration: Float = 0.5
        
        switch emotion {
        case .happy:
            // Анимация улыбки
            animateMouth(anchor: anchor, scaleY: 1.2, duration: duration)
        case .thinking:
            // Анимация размышлений
            animateHead(anchor: anchor, rotation: [0, 0.1, 0], duration: duration)
        case .explaining:
            // Анимация объяснения
            animateHead(anchor: anchor, position: [0, 0.02, 0], duration: duration)
        case .surprised:
            // Анимация удивления
            animateEyes(anchor: anchor, scale: 1.5, duration: duration)
        case .neutral:
            // Возврат в нейтральное состояние
            resetAnimations(anchor: anchor, duration: duration)
        }
    }
    
    private func animateMouth(anchor: AnchorEntity, scaleY: Float, duration: Float) {
        // Находим рот и анимируем его
        // В реальном приложении здесь была бы более сложная анимация
    }
    
    private func animateHead(anchor: AnchorEntity, rotation: SIMD3<Float>? = nil, position: SIMD3<Float>? = nil, duration: Float) {
        // Анимируем голову
    }
    
    private func animateEyes(anchor: AnchorEntity, scale: Float, duration: Float) {
        // Анимируем глаза
    }
    
    private func resetAnimations(anchor: AnchorEntity, duration: Float) {
        // Сбрасываем все анимации к базовому состоянию
    }
}

// Компонент для анимации аватара
struct AvatarAnimationComponent: Component {
    var isAnimating = false
    var currentAnimation: String = "idle"
}

// Типы эмоций для аватара
enum EmotionType {
    case neutral
    case happy
    case thinking
    case explaining
    case surprised
}

// Движок эмоций
class EmotionEngine: ObservableObject {
    @Published var currentEmotion: EmotionType = .neutral
    
    func setEmotion(_ emotion: EmotionType) {
        withAnimation(.easeInOut(duration: 0.3)) {
            currentEmotion = emotion
        }
    }
    
    func analyzeTextForEmotion(_ text: String) -> EmotionType {
        let lowercased = text.lowercased()
        
        if lowercased.contains("?") {
            return .thinking
        } else if lowercased.contains("!") {
            return .surprised
        } else if lowercased.contains("хорошо") || lowercased.contains("отлично") {
            return .happy
        } else if lowercased.contains("рекомендую") || lowercased.contains("советую") {
            return .explaining
        } else {
            return .neutral
        }
    }
}
'''

    def _generate_info_plist(self, app_name: str, bundle_id: str) -> str:
        """Генерирует Info.plist с необходимыми разрешениями"""
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>ru</string>
    <key>CFBundleDisplayName</key>
    <string>{app_name}</string>
    <key>CFBundleExecutable</key>
    <string>$(EXECUTABLE_NAME)</string>
    <key>CFBundleIdentifier</key>
    <string>{bundle_id}</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>$(PRODUCT_NAME)</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSRequiresIPhoneOS</key>
    <true/>
    
    <!-- Разрешения для голоса и микрофона -->
    <key>NSMicrophoneUsageDescription</key>
    <string>Приложение использует микрофон для распознавания ваших вопросов наставнику</string>
    <key>NSSpeechRecognitionUsageDescription</key>
    <string>Приложение использует распознавание речи для понимания ваших вопросов</string>
    
    <!-- Разрешения для камеры (для будущих функций AR) -->
    <key>NSCameraUsageDescription</key>
    <string>Камера используется для улучшенного взаимодействия с 3D наставником</string>
    
    <!-- Поддерживаемые интерфейсы -->
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
        <string>UIInterfaceOrientationLandscapeLeft</string>
        <string>UIInterfaceOrientationLandscapeRight</string>
    </array>
    
    <!-- Поддержка iPad -->
    <key>UISupportedInterfaceOrientations~ipad</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
        <string>UIInterfaceOrientationPortraitUpsideDown</string>
        <string>UIInterfaceOrientationLandscapeLeft</string>
        <string>UIInterfaceOrientationLandscapeRight</string>
    </array>
    
    <!-- Минимальная версия iOS -->
    <key>LSMinimumSystemVersion</key>
    <string>15.0</string>
    
    <!-- Поддержка темного режима -->
    <key>UIUserInterfaceStyle</key>
    <string>Automatic</string>
    
    <!-- Настройки сцены -->
    <key>UIApplicationSceneManifest</key>
    <dict>
        <key>UIApplicationSupportsMultipleScenes</key>
        <true/>
        <key>UISceneConfigurations</key>
        <dict>
            <key>UIWindowSceneSessionRoleApplication</key>
            <array>
                <dict>
                    <key>UISceneConfigurationName</key>
                    <string>Default Configuration</string>
                    <key>UISceneDelegateClassName</key>
                    <string>$(PRODUCT_MODULE_NAME).SceneDelegate</string>
                </dict>
            </array>
        </dict>
    </dict>
</dict>
</plist>
'''

    def _generate_spm_dependencies(self, features: List[str]) -> str:
        """Генерирует Package.swift с зависимостями"""
        return '''// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "AIMentorApp",
    platforms: [
        .iOS(.v15)
    ],
    products: [
        .library(
            name: "AIMentorApp",
            targets: ["AIMentorApp"]),
    ],
    dependencies: [
        // OpenAI для AI функциональности
        .package(url: "https://github.com/MacPaw/OpenAI", from: "0.6.0"),
        
        // Alamofire для сетевых запросов
        .package(url: "https://github.com/Alamofire/Alamofire.git", from: "5.8.0"),
        
        // SwiftUI дополнения
        .package(url: "https://github.com/siteline/SwiftUI-Introspect", from: "0.12.0"),
        
        // Анимации
        .package(url: "https://github.com/airbnb/lottie-ios.git", from: "4.3.0"),
        
        // Базы данных
        .package(url: "https://github.com/stephencelis/SQLite.swift.git", from: "0.14.1"),
        
        // JSON обработка
        .package(url: "https://github.com/SwiftyJSON/SwiftyJSON.git", from: "5.0.1"),
        
        // Keychain для безопасности
        .package(url: "https://github.com/evgenyneu/keychain-swift.git", from: "20.0.0"),
    ],
    targets: [
        .target(
            name: "AIMentorApp",
            dependencies: [
                "OpenAI",
                "Alamofire",
                .product(name: "SwiftUIIntrospect", package: "SwiftUI-Introspect"),
                .product(name: "Lottie", package: "lottie-ios"),
                .product(name: "SQLite", package: "SQLite.swift"),
                "SwiftyJSON",
                .product(name: "KeychainSwift", package: "keychain-swift")
            ]),
        .testTarget(
            name: "AIMentorAppTests",
            dependencies: ["AIMentorApp"]),
    ]
)
'''

    def generate_android_mentor_app(self, app_name: str, features: List[str]) -> Dict[str, str]:
        """Создает полный Android проект AI наставника"""
        
        package_name = f"com.aimentor.{app_name.lower().replace(' ', '').replace('-', '')}"
        
        return {
            # GRADLE КОНФИГУРАЦИЯ
            'build.gradle': self._generate_android_build_gradle(app_name, package_name),
            'app/build.gradle': self._generate_app_build_gradle(package_name),
            'gradle.properties': self._generate_gradle_properties(),
            'settings.gradle': self._generate_settings_gradle(app_name),
            
            # MANIFEST И РЕСУРСЫ
            'app/src/main/AndroidManifest.xml': self._generate_android_manifest(package_name, app_name),
            'app/src/main/res/values/strings.xml': self._generate_android_strings(app_name),
            'app/src/main/res/values/colors.xml': self._generate_android_colors(),
            'app/src/main/res/values/themes.xml': self._generate_android_themes(),
            
            # KOTLIN АКТИВНОСТИ
            f'app/src/main/java/{package_name.replace(".", "/")}/MainActivity.kt': self._generate_main_activity(package_name),
            f'app/src/main/java/{package_name.replace(".", "/")}/ui/screens/MentorSelectionScreen.kt': self._generate_mentor_selection_screen(package_name),
            f'app/src/main/java/{package_name.replace(".", "/")}/ui/screens/ChatScreen.kt': self._generate_chat_screen(package_name),
            
            # МОДЕЛИ ДАННЫХ
            f'app/src/main/java/{package_name.replace(".", "/")}/models/MentorModel.kt': self._generate_android_mentor_model(package_name),
            f'app/src/main/java/{package_name.replace(".", "/")}/models/MessageModel.kt': self._generate_android_message_model(package_name),
            
            # СЕРВИСЫ
            f'app/src/main/java/{package_name.replace(".", "/")}/services/VoiceService.kt': self._generate_android_voice_service(package_name),
            f'app/src/main/java/{package_name.replace(".", "/")}/services/AIService.kt': self._generate_android_ai_service(package_name),
            f'app/src/main/java/{package_name.replace(".", "/")}/services/TTSService.kt': self._generate_android_tts_service(package_name),
            
            # 3D МОДУЛЬ
            f'app/src/main/java/{package_name.replace(".", "/")}/graphics/Avatar3DRenderer.kt': self._generate_android_3d_renderer(package_name),
            
            # ДОКУМЕНТАЦИЯ
            'README.md': self._generate_android_readme(app_name, features)
        }

# Продолжение следует...