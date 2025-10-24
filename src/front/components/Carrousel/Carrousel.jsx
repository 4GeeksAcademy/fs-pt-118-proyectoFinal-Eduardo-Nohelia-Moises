import React, { useEffect, useMemo, useRef, useState } from "react";
import "./Carrousel.css";

// Carrousel con 20 fotografías y delay de 10 segundos entre fotos
export const Carrousel = () => {
  // Cargar imágenes desde assets/carrousel usando Vite import.meta.glob
  const modules = useMemo(() => (
    import.meta.glob("../assets/carrousel/*.{jpg,jpeg,png,svg}", { eager: true })
  ), []);
  const imagesFromAssets = useMemo(() => (
    Object.values(modules).map((m) => m.default)
  ), [modules]);

  // Asegurar 20 imágenes repitiendo si hay menos
  const images = useMemo(() => {
    const srcs = [];
    while (srcs.length < 20 && imagesFromAssets.length > 0) {
      srcs.push(...imagesFromAssets);
    }
    return (srcs.length ? srcs.slice(0, 20) : imagesFromAssets);
  }, [imagesFromAssets]);

  const [index, setIndex] = useState(0);
  const timerRef = useRef(null);
  const delayMs = 10000; // 10s entre fotos

  useEffect(() => {
    if (!images || images.length === 0) return;
    // autoplay: avanza cada 10s
    timerRef.current = setInterval(() => {
      setIndex((prev) => (prev + 1) % images.length);
    }, delayMs);
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [images.length]);

  // Controles manuales
  const prev = () => setIndex((prev) => (prev - 1 + images.length) % images.length);
  const next = () => setIndex((prev) => (prev + 1) % images.length);

  return (
    <div className="carrousel" aria-roledescription="carousel">
      <div className="carrousel-track" style={{ transform: `translateX(-${index * 100}%)` }}>
        {images.map((src, i) => (
          <div className="carrousel-slide" key={i} aria-hidden={i !== index}>
            <img src={src} alt={`Foto ${i + 1}`} loading="lazy" />
          </div>
        ))}
      </div>
      <div className="carrousel-controls">
        <button className="btn btn-sm btn-outline-light" onClick={prev} aria-label="Anterior">◀</button>
        <span className="carrousel-indicator">{index + 1} / {images.length}</span>
        <button className="btn btn-sm btn-outline-light" onClick={next} aria-label="Siguiente">▶</button>
      </div>
    </div>
  );
};